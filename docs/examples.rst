Examples
========

This section provides practical examples of using the Whole Slide Image Annotation Extractor.

Example 1: Basic Batch Processing
---------------------------------

Process all slides in a directory with default settings::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir /data/slides \
        --geojson_dir /data/annotations \
        --output_dir /data/output

This will:
* Find all slide images in ``/data/slides``
* Match them with GeoJSON files in ``/data/annotations``
* Generate 2000x2000 pixel tiles
* Save all tiles and masks to ``/data/output``

Example 2: Extract Only Annotated Tiles
----------------------------------------

Save only tiles that contain annotations::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir /data/slides \
        --geojson_dir /data/annotations \
        --output_dir /data/output \
        --only_annotated

This is useful when you only want tiles with annotations for training machine learning models.

Example 3: Custom Tile Size
----------------------------

Use smaller tiles (1024x1024) for faster processing::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir /data/slides \
        --geojson_dir /data/annotations \
        --output_dir /data/output \
        --tile_size 1024

Example 4: Process Specific File Types
---------------------------------------

Process only TIF and SVS files::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir /data/slides \
        --geojson_dir /data/annotations \
        --output_dir /data/output \
        --extensions .tif,.svs

Example 5: Programmatic Usage
------------------------------

Use the functions programmatically in a Python script::

    from batch_geojson_to_tiles_and_masks import (
        load_geojson,
        find_matching_geojson,
        create_tiles_and_masks_for_slide
    )
    import os

    # Define paths
    slides_dir = '/data/slides'
    geojson_dir = '/data/annotations'
    output_dir = '/data/output'

    # Process a single slide
    slide_path = os.path.join(slides_dir, 'DR123_slide.tif')
    geojson_path = find_matching_geojson(slide_path, geojson_dir)

    if geojson_path:
        annotations = load_geojson(geojson_path)
        stats = create_tiles_and_masks_for_slide(
            slide_path,
            annotations,
            output_dir,
            tile_size=2000,
            save_only_annotated=True
        )
        print(f"Processed {stats['filename']}")
        print(f"Saved {stats['saved_tiles']} tiles")

Example 6: Custom Mask Values
------------------------------

Use custom mask values for different annotation types::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir /data/slides \
        --geojson_dir /data/annotations \
        --output_dir /data/output \
        --mask_value 255 \
        --background_value 0

Example 7: Processing Different Slide Formats
----------------------------------------------

The tool automatically handles different slide formats. Here's an example directory structure::

    slides/
    ├── DR123_slide.tif
    ├── DR124_slide.svs
    ├── B1234567_slide.ndpi
    └── ABC12_slide.scn

    annotations/
    ├── DR123_annotation.geojson
    ├── DR124_annotation.geojson
    ├── B1234567_annotation.geojson
    └── ABC12_annotation.geojson

All these slides will be processed automatically::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir slides \
        --geojson_dir annotations \
        --output_dir output

Example 8: Understanding Output Structure
------------------------------------------

After processing, your output directory will look like::

    output/
    ├── DR123_slide/
    │   ├── tiles/
    │   │   ├── Da0.jpg
    │   │   ├── Da1.jpg
    │   │   ├── Da2.jpg
    │   │   └── ...
    │   └── masks/
    │       ├── Da0_mask.png
    │       ├── Da1_mask.png
    │       ├── Da2_mask.png
    │       └── ...
    ├── DR124_slide/
    │   └── ...
    └── batch_processing_summary.csv

The CSV file contains statistics::

    filename,total_tiles,tiles_with_annotations,saved_tiles,tiles_dir,masks_dir
    DR123_slide,150,45,45,output/DR123_slide/tiles,output/DR123_slide/masks
    DR124_slide,200,60,60,output/DR124_slide/tiles,output/DR124_slide/masks

Troubleshooting
---------------

**Problem**: No matching GeoJSON found

**Solution**: Check that your filenames follow the matching convention:
* Slides starting with 'DR': first 5 characters must match
* Slides starting with 'B': first 8 characters must match
* Other slides: first 5 characters must match

**Problem**: Memory errors when processing large slides

**Solution**: 
* Use smaller tile sizes (e.g., ``--tile_size 1024``)
* Process slides one at a time
* Ensure sufficient system memory

**Problem**: Tiles are not being saved

**Solution**: 
* Check that annotations actually intersect with tiles
* Verify ``--only_annotated`` flag is not set if you want all tiles
* Check write permissions for output directory

