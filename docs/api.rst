API Reference
=============

This section provides detailed documentation for all functions and classes in the module.

Core Functions
--------------

.. automodule:: batch_geojson_to_tiles_and_masks
   :members:
   :undoc-members:
   :show-inheritance:

Function Details
----------------

load_geojson
~~~~~~~~~~~~

.. autofunction:: batch_geojson_to_tiles_and_masks.load_geojson

Loads a GeoJSON file and extracts all polygon annotations.

**Parameters:**
    * ``geojson_path`` (str): Path to the GeoJSON file

**Returns:**
    * ``list``: List of Shapely polygon objects representing annotations

**Example:** ::

    annotations = load_geojson('annotations.geojson')
    print(f"Loaded {len(annotations)} annotations")

find_matching_geojson
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: batch_geojson_to_tiles_and_masks.find_matching_geojson

Finds a matching GeoJSON file for a slide image based on filename prefix matching.

**Parameters:**
    * ``slide_path`` (str): Path to the slide image file
    * ``geojson_dir`` (str): Directory containing GeoJSON files

**Returns:**
    * ``str`` or ``None``: Path to matching GeoJSON file, or None if not found

**Matching Rules:**
    * Slides starting with ``DR``: Match on first 5 characters
    * Slides starting with ``B``: Match on first 8 characters
    * Other slides: Match on first 5 characters (default)

**Example:** ::

    geojson_path = find_matching_geojson('DR123_slide.tif', '/path/to/geojson')
    if geojson_path:
        print(f"Found matching GeoJSON: {geojson_path}")

load_slide_image
~~~~~~~~~~~~~~~~

.. autofunction:: batch_geojson_to_tiles_and_masks.load_slide_image

Loads a whole slide image using tifffile and converts it to BGR format for OpenCV compatibility.

**Parameters:**
    * ``slide_path`` (str): Path to the slide image file

**Returns:**
    * ``numpy.ndarray``: Slide image in BGR format (height, width, 3)

**Supported Formats:**
    * Grayscale (converted to BGR)
    * RGB (converted to BGR)
    * RGBA (converted to BGR)

**Raises:**
    * ``ValueError``: If the slide image cannot be loaded

**Example:** ::

    slide = load_slide_image('slide.tif')
    print(f"Slide shape: {slide.shape}")

get_bounding_box_from_polygon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: batch_geojson_to_tiles_and_masks.get_bounding_box_from_polygon

Extracts bounding box coordinates from a Shapely polygon.

**Parameters:**
    * ``polygon``: Shapely polygon object

**Returns:**
    * ``tuple``: (x_min, y_min, x_max, y_max)

**Example:** ::

    bbox = get_bounding_box_from_polygon(polygon)
    x_min, y_min, x_max, y_max = bbox

create_tiles_and_masks_for_slide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: batch_geojson_to_tiles_and_masks.create_tiles_and_masks_for_slide

Creates tile images and corresponding mask tiles for a single slide.

**Parameters:**
    * ``slide_path`` (str): Path to the whole slide image
    * ``annotations`` (list): List of annotation polygons from GeoJSON
    * ``output_dir`` (str): Output directory for tiles and masks
    * ``tile_size`` (int, optional): Size of output tiles in pixels (default: 2000)
    * ``mask_value`` (int, optional): Pixel value for annotated regions (default: 255)
    * ``background_value`` (int, optional): Pixel value for background (default: 0)
    * ``save_only_annotated`` (bool, optional): Only save tiles with annotations (default: False)

**Returns:**
    * ``dict``: Statistics dictionary with keys:
        * ``filename``: Slide basename
        * ``total_tiles``: Total number of tiles processed
        * ``tiles_with_annotations``: Number of tiles containing annotations
        * ``saved_tiles``: Number of tiles saved
        * ``tiles_dir``: Path to tiles directory
        * ``masks_dir``: Path to masks directory

**Example:** ::

    stats = create_tiles_and_masks_for_slide(
        'slide.tif',
        annotations,
        'output/',
        tile_size=2000,
        save_only_annotated=True
    )
    print(f"Saved {stats['saved_tiles']} tiles")

process_batch
~~~~~~~~~~~~~

.. autofunction:: batch_geojson_to_tiles_and_masks.process_batch

Processes a batch of slides and their matching GeoJSON files.

**Parameters:**
    * ``slides_dir`` (str): Directory containing slide images
    * ``geojson_dir`` (str): Directory containing GeoJSON files
    * ``output_dir`` (str): Output directory for all tiles and masks
    * ``tile_size`` (int, optional): Size of output tiles (default: 2000)
    * ``mask_value`` (int, optional): Pixel value for annotated regions (default: 255)
    * ``background_value`` (int, optional): Pixel value for background (default: 0)
    * ``save_only_annotated`` (bool, optional): Only save tiles with annotations (default: False)
    * ``slide_extensions`` (list, optional): List of file extensions to process
      (default: ['.tif', '.tiff', '.svs', '.ndpi', '.scn', '.mrxs', '.jpg', '.png'])

**Returns:**
    * ``None``: Statistics are printed to console and saved to CSV

**Output:**
    * Creates tile and mask files for each processed slide
    * Generates ``batch_processing_summary.csv`` in the output directory

**Example:** ::

    process_batch(
        'slides/',
        'annotations/',
        'output/',
        tile_size=2000,
        save_only_annotated=False
    )

Data Structures
---------------

Statistics Dictionary
~~~~~~~~~~~~~~~~~~~~~

The statistics dictionary returned by ``create_tiles_and_masks_for_slide`` has the following structure::

    {
        'filename': str,              # Slide basename without extension
        'total_tiles': int,            # Total number of tiles processed
        'tiles_with_annotations': int, # Number of tiles containing annotations
        'saved_tiles': int,            # Number of tiles actually saved
        'tiles_dir': str,              # Path to tiles directory
        'masks_dir': str               # Path to masks directory
    }

