# Building the Documentation

This directory contains the Sphinx documentation for the Whole Slide Image Annotation Extractor.

## Prerequisites

Install Sphinx and the required theme::

    pip install sphinx sphinx-rtd-theme

## Building the Documentation

### On Linux/macOS

Use the Makefile::

    make html

### On Windows

Use the batch file::

    make.bat html

### Alternative (All Platforms)

You can also use sphinx-build directly::

    sphinx-build -b html . _build/html

## Viewing the Documentation

After building, open `_build/html/index.html` in your web browser.

## Available Build Targets

* `html` - Build HTML documentation
* `latex` - Build LaTeX documentation
* `pdf` - Build PDF documentation (requires LaTeX)
* `clean` - Remove build files
* `help` - Show available build targets

## Documentation Structure

* `index.rst` - Main documentation entry point
* `overview.rst` - Overview of the project
* `installation.rst` - Installation instructions
* `usage.rst` - Usage guide and command-line interface
* `api.rst` - API reference documentation
* `examples.rst` - Usage examples and tutorials

## Publishing to GitHub Pages

To publish the documentation to GitHub Pages:

1. Build the HTML documentation::

    make html

2. Copy the contents of `_build/html` to your `gh-pages` branch or to the `docs` folder in your main branch.

3. GitHub will automatically serve the documentation from the `docs` folder if enabled in repository settings.

