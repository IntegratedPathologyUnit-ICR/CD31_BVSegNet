import numpy as np
import cv2
import json
import os
import math
import argparse
from pathlib import Path
from shapely.geometry import shape, Point, Polygon
import tifffile
import glob
import pandas as pd


def load_geojson(geojson_path):
    """
    Load GeoJSON file and extract rectangular annotations.
    
    Parameters:
    geojson_path (str): Path to GeoJSON file
    
    Returns:
    list: List of annotation polygons
    """
    with open(geojson_path, 'r') as f:
        data = json.load(f)
    
    annotations = []
    for feature in data['features']:
        geom = shape(feature['geometry'])
        annotations.append(geom)
    
    print(f"Loaded {len(annotations)} annotations from GeoJSON")
    return annotations


def find_matching_geojson(slide_path, geojson_dir):
    """
    Find matching GeoJSON file based on slide filename prefix.
    - If slide starts with 'DR': match on first 5 characters
    - If slide starts with 'B': match on first 8 characters
    - Otherwise: match on first 5 characters (default)
    
    Parameters:
    slide_path (str): Path to slide image
    geojson_dir (str): Directory containing GeoJSON files
    
    Returns:
    str: Path to matching GeoJSON file or None if not found
    """
    slide_basename = os.path.basename(slide_path)
    
    # Determine the number of characters to match based on prefix
    if slide_basename.startswith('DR'):
        prefix_length = 5
    elif slide_basename.startswith('B'):
        prefix_length = 8
    else:
        prefix_length = 5  # Default
    
    slide_prefix = slide_basename[:prefix_length]
    
    # Search for GeoJSON files in the directory
    geojson_files = glob.glob(os.path.join(geojson_dir, "*.geojson"))
    
    for geojson_file in geojson_files:
        geojson_basename = os.path.basename(geojson_file)
        geojson_prefix = geojson_basename[:prefix_length]
        
        if slide_prefix == geojson_prefix:
            print(f"Matched slide '{slide_basename}' with GeoJSON '{geojson_basename}' "
                  f"(prefix: '{slide_prefix}', length: {prefix_length})")
            return geojson_file
    
    return None


def load_slide_image(slide_path):
    """
    Load slide image using tifffile.
    
    Parameters:
    slide_path (str): Path to slide image
    
    Returns:
    np.array: Slide image in BGR format (for consistency with OpenCV)
    """
    print(f"Loading slide image: {slide_path}")
    slide = tifffile.imread(slide_path)
    
    if slide is None:
        raise ValueError(f"Could not load slide image from {slide_path}")
    
    print(f"Original slide shape: {slide.shape}, dtype: {slide.dtype}")
    
    # Handle different image formats
    if len(slide.shape) == 2:
        # Grayscale image, convert to BGR
        slide = cv2.cvtColor(slide, cv2.COLOR_GRAY2BGR)
        print("Converted grayscale to BGR")
    elif len(slide.shape) == 3:
        if slide.shape[2] == 4:
            # RGBA image, convert to BGR
            slide = cv2.cvtColor(slide, cv2.COLOR_RGBA2BGR)
            print("Converted RGBA to BGR")
        elif slide.shape[2] == 3:
            # Assume RGB, convert to BGR for consistency with OpenCV
            slide = cv2.cvtColor(slide, cv2.COLOR_RGB2BGR)
            print("Converted RGB to BGR")
    
    slide_height, slide_width = slide.shape[:2]
    print(f"Slide dimensions: {slide_width} x {slide_height}")
    
    return slide


def get_bounding_box_from_polygon(polygon):
    """
    Get bounding box coordinates from a polygon.
    
    Parameters:
    polygon: Shapely polygon
    
    Returns:
    tuple: (x_min, y_min, x_max, y_max)
    """
    bounds = polygon.bounds  # Returns (minx, miny, maxx, maxy)
    return bounds


def create_tiles_and_masks_for_slide(slide_path, annotations, output_dir, tile_size=2000, 
                                      mask_value=255, background_value=0, 
                                      save_only_annotated=False):
    """
    Create tile images and corresponding mask tiles for a single slide.
    
    Parameters:
    slide_path (str): Path to the whole slide image
    annotations (list): List of annotation polygons from GeoJSON
    output_dir (str): Output directory for tiles and masks
    tile_size (int): Size of output tiles (default 2000x2000)
    mask_value (int): Pixel value for annotated regions in mask (default 255)
    background_value (int): Pixel value for background in mask (default 0)
    save_only_annotated (bool): If True, only save tiles that contain annotations
    
    Returns:
    dict: Statistics about the processed slide
    """
    # Get slide basename for naming
    slide_basename = os.path.splitext(os.path.basename(slide_path))[0]
    
    # Create output directories for this slide
    slide_output_dir = os.path.join(output_dir, slide_basename)
    tiles_dir = os.path.join(slide_output_dir, 'tiles')
    masks_dir = os.path.join(slide_output_dir, 'masks')
    Path(tiles_dir).mkdir(parents=True, exist_ok=True)
    Path(masks_dir).mkdir(parents=True, exist_ok=True)
    
    # Load the slide image using tifffile
    slide = load_slide_image(slide_path)
    slide_height, slide_width = slide.shape[:2]
    
    # Calculate number of tiles needed
    num_tiles_x = math.ceil(slide_width / tile_size)
    num_tiles_y = math.ceil(slide_height / tile_size)
    total_tiles = num_tiles_x * num_tiles_y
    
    print(f"Will process {num_tiles_x} x {num_tiles_y} = {total_tiles} tiles")
    if save_only_annotated:
        print("Only saving tiles with annotations")
    
    tile_index = 0
    saved_tiles = 0
    tiles_with_annotations = 0
    
    # Generate tiles
    for row in range(num_tiles_y):
        for col in range(num_tiles_x):
            # Calculate tile position
            x_start = col * tile_size
            y_start = row * tile_size
            x_end = min(x_start + tile_size, slide_width)
            y_end = min(y_start + tile_size, slide_height)
            
            # Extract tile from slide
            tile = slide[y_start:y_end, x_start:x_end]
            
            # Create a full-sized tile (pad if necessary for border tiles)
            tile_full = np.zeros((tile_size, tile_size, 3), dtype=np.uint8)
            actual_height, actual_width = tile.shape[:2]
            tile_full[:actual_height, :actual_width] = tile
            
            # Create mask for this tile
            mask = np.zeros((tile_size, tile_size), dtype=np.uint8) + background_value
            
            # Check which annotations intersect with this tile
            tile_bbox = Polygon([
                [x_start, y_start],
                [x_end, y_start],
                [x_end, y_end],
                [x_start, y_end],
                [x_start, y_start]
            ])
            
            has_annotation = False
            
            for annotation in annotations:
                # Check if annotation intersects with this tile
                if annotation.intersects(tile_bbox):
                    has_annotation = True
                    
                    # Get the intersection
                    intersection = annotation.intersection(tile_bbox)
                    
                    # Convert to local tile coordinates
                    if intersection.geom_type == 'Polygon':
                        polys_to_draw = [intersection]
                    elif intersection.geom_type == 'MultiPolygon':
                        polys_to_draw = list(intersection.geoms)
                    else:
                        continue
                    
                    for poly in polys_to_draw:
                        # Get coordinates and convert to local tile coordinates
                        coords = np.array(poly.exterior.coords)
                        local_coords = coords - [x_start, y_start]
                        local_coords = local_coords.astype(np.int32)
                        
                        # Fill the polygon in the mask
                        cv2.fillPoly(mask, [local_coords], mask_value)
            
            # Decide whether to save this tile
            should_save = not save_only_annotated or has_annotation
            
            if should_save:
                # Save tile and mask with Da{tile_index} naming
                tile_filename = f"Da{tile_index}.jpg"
                mask_filename = f"Da{tile_index}_mask.png"
                
                tile_path = os.path.join(tiles_dir, tile_filename)
                mask_path = os.path.join(masks_dir, mask_filename)
                
                cv2.imwrite(tile_path, tile_full)
                cv2.imwrite(mask_path, mask)
                
                saved_tiles += 1
            
            if has_annotation:
                tiles_with_annotations += 1
            
            tile_index += 1
            
            if tile_index % 100 == 0:
                print(f"  Processed {tile_index}/{total_tiles} tiles "
                      f"({tiles_with_annotations} with annotations, {saved_tiles} saved)")
    
    print(f"Slide processing complete!")
    print(f"  Processed {tile_index} tiles total")
    print(f"  {tiles_with_annotations} tiles contain annotations")
    print(f"  Saved {saved_tiles} tiles")
    print(f"  Tiles saved to: {tiles_dir}")
    print(f"  Masks saved to: {masks_dir}")
    
    return {
        'filename': slide_basename,
        'total_tiles': tile_index,
        'tiles_with_annotations': tiles_with_annotations,
        'saved_tiles': saved_tiles,
        'tiles_dir': tiles_dir,
        'masks_dir': masks_dir
    }


def process_batch(slides_dir, geojson_dir, output_dir, tile_size=2000, 
                  mask_value=255, background_value=0, save_only_annotated=False,
                  slide_extensions=None):
    """
    Process a batch of slides and their matching GeoJSON files.
    
    Parameters:
    slides_dir (str): Directory containing slide images
    geojson_dir (str): Directory containing GeoJSON files
    output_dir (str): Output directory for all tiles and masks
    tile_size (int): Size of output tiles (default 2000x2000)
    mask_value (int): Pixel value for annotated regions in mask (default 255)
    background_value (int): Pixel value for background in mask (default 0)
    save_only_annotated (bool): If True, only save tiles that contain annotations
    slide_extensions (list): List of slide file extensions to process
    """
    if slide_extensions is None:
        slide_extensions = ['.tif', '.tiff', '.svs', '.ndpi', '.scn', '.mrxs', '.jpg', '.png']
    
    # Find all slide files
    slide_files = []
    for ext in slide_extensions:
        slide_files.extend(glob.glob(os.path.join(slides_dir, f"*{ext}")))
        slide_files.extend(glob.glob(os.path.join(slides_dir, f"*{ext.upper()}")))
    
    slide_files = sorted(list(set(slide_files)))  # Remove duplicates and sort
    
    print(f"Found {len(slide_files)} slide files in {slides_dir}")
    print(f"Looking for matching GeoJSON files in {geojson_dir}")
    print("=" * 80)
    
    processed_count = 0
    skipped_count = 0
    batch_stats = []
    
    for idx, slide_path in enumerate(slide_files, 1):
        slide_basename = os.path.basename(slide_path)
        print(f"\n[{idx}/{len(slide_files)}] Processing slide: {slide_basename}")
        print("-" * 80)
        
        # Find matching GeoJSON file
        geojson_path = find_matching_geojson(slide_path, geojson_dir)
        
        if geojson_path is None:
            # Determine prefix length for error message
            if slide_basename.startswith('DR'):
                prefix_length = 5
            elif slide_basename.startswith('B'):
                prefix_length = 8
            else:
                prefix_length = 5
            
            print(f"WARNING: No matching GeoJSON found for '{slide_basename}' "
                  f"(prefix: '{slide_basename[:prefix_length]}', length: {prefix_length})")
            print(f"Skipping this slide.")
            skipped_count += 1
            continue
        
        try:
            # Load annotations
            annotations = load_geojson(geojson_path)
            
            if len(annotations) == 0:
                print(f"WARNING: No annotations found in GeoJSON file. Skipping this slide.")
                skipped_count += 1
                continue
            
            # Process the slide
            stats = create_tiles_and_masks_for_slide(
                slide_path,
                annotations,
                output_dir,
                tile_size=tile_size,
                mask_value=mask_value,
                background_value=background_value,
                save_only_annotated=save_only_annotated
            )
            
            batch_stats.append(stats)
            processed_count += 1
            
        except Exception as e:
            print(f"ERROR processing slide '{slide_basename}': {str(e)}")
            import traceback
            traceback.print_exc()
            skipped_count += 1
            continue
    
    # Print summary
    print("\n" + "=" * 80)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 80)
    print(f"Total slides found: {len(slide_files)}")
    print(f"Successfully processed: {processed_count}")
    print(f"Skipped: {skipped_count}")
    print()
    
    if batch_stats:
        print("Per-slide statistics:")
        print("-" * 80)
        total_tiles_all = 0
        total_annotated_all = 0
        total_saved_all = 0
        
        for stats in batch_stats:
            print(f"  {stats['filename']}:")
            print(f"    Total tiles: {stats['total_tiles']}")
            print(f"    Tiles with annotations: {stats['tiles_with_annotations']}")
            print(f"    Saved tiles: {stats['saved_tiles']}")
            
            total_tiles_all += stats['total_tiles']
            total_annotated_all += stats['tiles_with_annotations']
            total_saved_all += stats['saved_tiles']
        
        print("-" * 80)
        print(f"TOTALS:")
        print(f"  Total tiles processed: {total_tiles_all}")
        print(f"  Total tiles with annotations: {total_annotated_all}")
        print(f"  Total tiles saved: {total_saved_all}")
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(batch_stats)
        csv_path = os.path.join(output_dir, 'batch_processing_summary.csv')
        df.to_csv(csv_path, index=False)
        print()
        print(f"Statistics saved to: {csv_path}")
        print()
        print("CSV Preview:")
        print(df[['filename', 'total_tiles', 'tiles_with_annotations', 'saved_tiles']].to_string(index=False))
    
    print("=" * 80)
    print(f"Output saved to: {output_dir}")


if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description='Batch process slides and create tiles/masks from GeoJSON annotations (using tifffile)'
    )
    parser.add_argument('--slides_dir', required=True, 
                       help='Directory containing slide images')
    parser.add_argument('--geojson_dir', required=True, 
                       help='Directory containing GeoJSON files')
    parser.add_argument('--output_dir', required=True, 
                       help='Output directory for all tiles and masks')
    parser.add_argument('--tile_size', type=int, default=2000, 
                       help='Size of output tiles (default 2000x2000)')
    parser.add_argument('--mask_value', type=int, default=255, 
                       help='Pixel value for annotated regions in mask (default 255)')
    parser.add_argument('--background_value', type=int, default=0, 
                       help='Pixel value for background in mask (default 0)')
    parser.add_argument('--only_annotated', action='store_true',
                       help='Only save tiles that contain annotations')
    parser.add_argument('--extensions', type=str, default='.tif,.tiff,.svs,.ndpi,.scn,.mrxs,.jpg,.png',
                       help='Comma-separated list of slide file extensions (default: .tif,.tiff,.svs,.ndpi,.scn,.mrxs,.jpg,.png)')
    
    args = parser.parse_args()
    
    # Parse extensions
    slide_extensions = [ext.strip() for ext in args.extensions.split(',')]
    
    # Process the batch
    process_batch(
        args.slides_dir,
        args.geojson_dir,
        args.output_dir,
        tile_size=args.tile_size,
        mask_value=args.mask_value,
        background_value=args.background_value,
        save_only_annotated=args.only_annotated,
        slide_extensions=slide_extensions
    )
