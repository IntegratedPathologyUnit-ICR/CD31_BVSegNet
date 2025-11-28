import numpy as np
import cv2
import json
import os
import math
import argparse
from pathlib import Path
from shapely.geometry import shape, Point, Polygon
import tifffile


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


def create_tiles_and_masks(slide_path, annotations, output_dir, tile_size=2000,
                           mask_value=255, background_value=0):
    """
    Create tile images and corresponding mask tiles from slide image and annotations.

    Parameters:
    slide_path (str): Path to the whole slide image
    annotations (list): List of annotation polygons from GeoJSON
    output_dir (str): Output directory for tiles and masks
    tile_size (int): Size of output tiles (default 2000x2000)
    mask_value (int): Pixel value for annotated regions in mask (default 255)
    background_value (int): Pixel value for background in mask (default 0)
    """
    # Create output directories
    tiles_dir = os.path.join(output_dir, 'tiles')
    masks_dir = os.path.join(output_dir, 'masks')
    Path(tiles_dir).mkdir(parents=True, exist_ok=True)
    Path(masks_dir).mkdir(parents=True, exist_ok=True)

    # Load the slide image using tifffile
    slide = load_slide_image(slide_path)
    slide_height, slide_width = slide.shape[:2]

    # Calculate number of tiles needed
    num_tiles_x = math.ceil(slide_width / tile_size)
    num_tiles_y = math.ceil(slide_height / tile_size)
    total_tiles = num_tiles_x * num_tiles_y

    print(f"Will create {num_tiles_x} x {num_tiles_y} = {total_tiles} tiles")

    tile_count = 0
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

            # Save tile and mask with Da{tile_count} naming
            tile_filename = f"Da{tile_count}.jpg"
            mask_filename = f"Da{tile_count}_mask.png"

            tile_path = os.path.join(tiles_dir, tile_filename)
            mask_path = os.path.join(masks_dir, mask_filename)

            cv2.imwrite(tile_path, tile_full)
            cv2.imwrite(mask_path, mask)

            if has_annotation:
                tiles_with_annotations += 1

            tile_count += 1

            if tile_count % 100 == 0:
                print(f"Processed {tile_count}/{total_tiles} tiles ({tiles_with_annotations} with annotations)")

    print(f"\nProcessing complete!")
    print(f"Created {tile_count} tiles total")
    print(f"{tiles_with_annotations} tiles contain annotations")
    print(f"Tiles saved to: {tiles_dir}")
    print(f"Masks saved to: {masks_dir}")


def create_tiles_and_masks_filtered(slide_path, annotations, output_dir, tile_size=2000,
                                    mask_value=255, background_value=0,
                                    save_only_annotated=False):
    """
    Create tile images and corresponding mask tiles from slide image and annotations.
    Option to save only tiles that contain annotations.

    Parameters:
    slide_path (str): Path to the whole slide image
    annotations (list): List of annotation polygons from GeoJSON
    output_dir (str): Output directory for tiles and masks
    tile_size (int): Size of output tiles (default 2000x2000)
    mask_value (int): Pixel value for annotated regions in mask (default 255)
    background_value (int): Pixel value for background in mask (default 0)
    save_only_annotated (bool): If True, only save tiles that contain annotations
    """
    # Create output directories
    tiles_dir = os.path.join(output_dir, 'tiles')
    masks_dir = os.path.join(output_dir, 'masks')
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
                print(f"Processed {tile_index}/{total_tiles} tiles "
                      f"({tiles_with_annotations} with annotations, {saved_tiles} saved)")

    print(f"\nProcessing complete!")
    print(f"Processed {tile_index} tiles total")
    print(f"{tiles_with_annotations} tiles contain annotations")
    print(f"Saved {saved_tiles} tiles")
    print(f"Tiles saved to: {tiles_dir}")
    print(f"Masks saved to: {masks_dir}")


if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description='Create tile images and masks from GeoJSON annotations and slide image (using tifffile)'
    )
    parser.add_argument('--slide', required=True,
                        help='Path to the whole slide image (TIFF/TIF/etc)')
    parser.add_argument('--geojson', required=True,
                        help='Path to the GeoJSON file with annotations')
    parser.add_argument('--output_dir', required=True,
                        help='Output directory for tiles and masks')
    parser.add_argument('--tile_size', type=int, default=2000,
                        help='Size of output tiles (default 2000x2000)')
    parser.add_argument('--mask_value', type=int, default=255,
                        help='Pixel value for annotated regions in mask (default 255)')
    parser.add_argument('--background_value', type=int, default=0,
                        help='Pixel value for background in mask (default 0)')
    parser.add_argument('--only_annotated', action='store_true',
                        help='Only save tiles that contain annotations')

    args = parser.parse_args()

    # Load annotations from GeoJSON
    annotations = load_geojson(args.geojson)

    # Create tiles and masks
    create_tiles_and_masks_filtered(
        args.slide,
        annotations,
        args.output_dir,
        tile_size=args.tile_size,
        mask_value=args.mask_value,
        background_value=args.background_value,
        save_only_annotated=args.only_annotated
    )