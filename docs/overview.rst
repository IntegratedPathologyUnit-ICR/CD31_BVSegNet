Overview
========

The Whole Slide Image Annotation Extractor is designed to process histopathology whole slide images
and extract tiles based on annotations provided in GeoJSON format. This tool is particularly useful
for preparing training data for machine learning models in digital pathology.

Architecture
------------

The tool consists of several key components:

1. **File Matching**: Automatically matches slide images with their corresponding GeoJSON annotation files
   based on filename prefixes.

2. **Image Loading**: Loads whole slide images using tifffile, supporting multiple formats and color spaces.

3. **Annotation Processing**: Parses GeoJSON files to extract polygon annotations.

4. **Tile Extraction**: Divides whole slide images into tiles of specified size.

5. **Mask Generation**: Creates binary masks indicating annotated regions within each tile.

6. **Batch Processing**: Processes multiple slides and generates comprehensive statistics.

Workflow
--------

The typical workflow is as follows:

1. **Input Preparation**:
   - Organize slide images in a directory
   - Organize GeoJSON annotation files in a separate directory
   - Ensure filenames follow the matching convention

2. **Matching**:
   - The tool automatically matches slides with GeoJSON files based on filename prefixes
   - Different prefix lengths are used depending on the slide filename pattern

3. **Processing**:
   - Each slide is divided into tiles
   - For each tile, the tool checks if any annotations intersect with it
   - Tiles and corresponding masks are generated

4. **Output**:
   - Tiles are saved as JPG images
   - Masks are saved as PNG images
   - Statistics are collected and saved to CSV

Supported Formats
-----------------

**Slide Image Formats:**
* TIF/TIFF
* SVS (Aperio)
* NDPI (Hamamatsu)
* SCN (Leica)
* MRXS (3DHistech)
* JPG/JPEG
* PNG

**Annotation Format:**
* GeoJSON (with polygon geometries)

Output Structure
-----------------

The output directory structure is organized as follows::

    output_dir/
    ├── slide_name_1/
    │   ├── tiles/
    │   │   ├── Da0.jpg
    │   │   ├── Da1.jpg
    │   │   └── ...
    │   └── masks/
    │       ├── Da0_mask.png
    │       ├── Da1_mask.png
    │       └── ...
    ├── slide_name_2/
    │   └── ...
    └── batch_processing_summary.csv

Each tile is named with the pattern ``Da{index}.jpg`` and its corresponding mask is named
``Da{index}_mask.png``, where ``{index}`` is the sequential tile index.

