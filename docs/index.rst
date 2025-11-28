Whole Slide Image Annotation Extractor Documentation
====================================================

Welcome to the documentation for the Whole Slide Image Annotation Extractor.
This tool processes whole slide images (WSI) and extracts tiles based on GeoJSON annotations.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   installation
   usage
   api
   examples

Overview
--------

This project provides functionality to:

* Load and process whole slide images in various formats (TIF, SVS, NDPI, SCN, MRXS, JPG, PNG)
* Match slide images with corresponding GeoJSON annotation files using intelligent filename matching
* Extract tiles from whole slide images
* Generate binary masks for annotated regions
* Process multiple slides in batch mode

The tool supports different filename matching strategies:

* Slides starting with ``DR``: Match on first 5 characters
* Slides starting with ``B``: Match on first 8 characters
* Other slides: Match on first 5 characters (default)

Key Features
------------

* **Multi-format Support**: Handles various whole slide image formats
* **Intelligent Matching**: Automatic matching of slides with GeoJSON files based on filename prefixes
* **Flexible Tiling**: Configurable tile sizes and extraction options
* **Annotation Masks**: Generates binary masks for annotated regions
* **Batch Processing**: Process multiple slides efficiently
* **Statistics**: Comprehensive statistics and CSV output for processed slides

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

