Usage
=====

Command Line Interface
----------------------

The tool is primarily used via the command line interface. The main script is
``batch_geojson_to_tiles_and_masks.py``.

Basic Usage
-----------

The basic command structure is::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir <path_to_slides> \
        --geojson_dir <path_to_geojson> \
        --output_dir <path_to_output>

Required Arguments
------------------

* ``--slides_dir``: Directory containing whole slide images
* ``--geojson_dir``: Directory containing GeoJSON annotation files
* ``--output_dir``: Directory where tiles and masks will be saved

Optional Arguments
------------------

* ``--tile_size``: Size of output tiles in pixels (default: 2000)
* ``--mask_value``: Pixel value for annotated regions in mask (default: 255)
* ``--background_value``: Pixel value for background in mask (default: 0)
* ``--only_annotated``: Only save tiles that contain annotations
* ``--extensions``: Comma-separated list of slide file extensions to process
  (default: .tif,.tiff,.svs,.ndpi,.scn,.mrxs,.jpg,.png)

Examples
--------

Basic Processing
~~~~~~~~~~~~~~~~

Process all slides with default settings::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir /path/to/slides \
        --geojson_dir /path/to/geojson \
        --output_dir /path/to/output

Only Save Annotated Tiles
~~~~~~~~~~~~~~~~~~~~~~~~~

Only save tiles that contain annotations::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir /path/to/slides \
        --geojson_dir /path/to/geojson \
        --output_dir /path/to/output \
        --only_annotated

Custom Tile Size
~~~~~~~~~~~~~~~~

Use custom tile size (e.g., 1024x1024)::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir /path/to/slides \
        --geojson_dir /path/to/geojson \
        --output_dir /path/to/output \
        --tile_size 1024

Custom File Extensions
~~~~~~~~~~~~~~~~~~~~~~

Process only specific file types::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir /path/to/slides \
        --geojson_dir /path/to/geojson \
        --output_dir /path/to/output \
        --extensions .tif,.svs,.ndpi

Custom Mask Values
~~~~~~~~~~~~~~~~~~

Use custom mask values::

    python batch_geojson_to_tiles_and_masks.py \
        --slides_dir /path/to/slides \
        --geojson_dir /path/to/geojson \
        --output_dir /path/to/output \
        --mask_value 255 \
        --background_value 0

Filename Matching
-----------------

The tool automatically matches slide images with GeoJSON files based on filename prefixes:

* **Slides starting with 'DR'**: Matches on first 5 characters
  * Example: ``DR123_slide.tif`` matches ``DR123_annotation.geojson``

* **Slides starting with 'B'**: Matches on first 8 characters
  * Example: ``B1234567_slide.tif`` matches ``B1234567_annotation.geojson``

* **Other slides**: Matches on first 5 characters (default)
  * Example: ``ABC12_slide.tif`` matches ``ABC12_annotation.geojson``

Output
------

The tool generates:

1. **Tiles**: JPG images named ``Da{index}.jpg``
2. **Masks**: PNG images named ``Da{index}_mask.png``
3. **Statistics**: CSV file ``batch_processing_summary.csv`` with processing statistics

The statistics CSV includes:
* Filename
* Total tiles processed
* Tiles with annotations
* Saved tiles
* Output directories

Programmatic Usage
------------------

You can also use the functions programmatically::

    from batch_geojson_to_tiles_and_masks import (
        load_geojson,
        find_matching_geojson,
        load_slide_image,
        create_tiles_and_masks_for_slide,
        process_batch
    )

    # Load annotations
    annotations = load_geojson('path/to/annotation.geojson')

    # Load slide
    slide = load_slide_image('path/to/slide.tif')

    # Process single slide
    stats = create_tiles_and_masks_for_slide(
        'path/to/slide.tif',
        annotations,
        'path/to/output',
        tile_size=2000
    )

    # Process batch
    process_batch(
        'path/to/slides',
        'path/to/geojson',
        'path/to/output',
        tile_size=2000,
        save_only_annotated=False
    )

See the :doc:`api` section for detailed API documentation.

