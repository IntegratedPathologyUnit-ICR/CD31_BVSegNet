# BVSegNet

Immunohistochemistry whole slide image dissection for Blood vessel segmentation 

# Annotation extraction for training and validation

This workflow supports all images supported by tifffile library and the annotations are performed within the open-source qupath software (https://qupath.github.io/)

A Python tool for extracting tiles from whole slide images (WSI) based on GeoJSON annotations. This tool is designed for processing histopathology images and preparing training data and parsing for
supervised and unsupervised learning models.

## Features

* **Multi-format Support**: Handles various whole slide image formats (TIF, SVS, NDPI, SCN, MRXS, JPG, PNG)
* **Intelligent Matching**: Automatic matching of slides with GeoJSON files based on filename prefixes
* **Flexible Tiling**: Configurable tile sizes and extraction options
* **Annotation Masks**: Generates binary masks for annotated regions
* **Batch Processing**: Process multiple slides efficiently
* **Statistics**: Comprehensive statistics and CSV output for processed slides

## Quick Start

### Installation

```bash
pip install numpy opencv-python shapely tifffile pandas
```

### Basic Usage

```bash
python batch_geojson_to_tiles_and_masks.py \
    --slides_dir /path/to/slides \
    --geojson_dir /path/to/geojson \
    --output_dir /path/to/output
```

## Documentation

### Local Build

Full documentation is available in the `docs/` directory. To build the documentation locally:

```bash
cd docs
pip install -r ../requirements-docs.txt
make html  # or make.bat html on Windows
```

Then open `docs/_build/html/index.html` in your browser.

### Online Documentation

**Read the Docs**: The documentation is automatically built and hosted on Read the Docs at:
https://your-project-name.readthedocs.io/

See [README_RTD.md](README_RTD.md) for instructions on connecting your repository to Read the Docs.

**GitHub Pages**: Alternatively, you can host on GitHub Pages by copying `docs/_build/html/*` to a `docs/` folder in your repository.

## Filename Matching

The tool automatically matches slide images with GeoJSON files:

* **Slides starting with 'DR'**: Match on first 5 characters
* **Slides starting with 'B'**: Match on first 8 characters
* **Other slides**: Match on first 5 characters (default)

## Requirements

* Python 3.7+
* numpy
* opencv-python
* shapely
* tifffile
* pandas

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Citation

If you use this tool in your research, please cite:

```
[Add citation information]
```


