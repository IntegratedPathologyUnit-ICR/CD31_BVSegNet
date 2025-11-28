Installation
============

Prerequisites
-------------

* Python 3.7 or higher
* pip (Python package installer)

Required Dependencies
---------------------

Install the required packages using pip::

    pip install numpy opencv-python shapely tifffile pandas

Or install from a requirements file (see :ref:`requirements-file`).

Installation Steps
------------------

1. **Clone or download the repository**::

    git clone <repository-url>
    cd Driven_paper

2. **Install dependencies**::

    pip install -r requirements.txt

3. **Verify installation**::

    python batch_geojson_to_tiles_and_masks.py --help

Requirements File
-----------------

.. _requirements-file:

Create a ``requirements.txt`` file with the following content::

    numpy>=1.20.0
    opencv-python>=4.5.0
    shapely>=1.8.0
    tifffile>=2021.0.0
    pandas>=1.3.0

Then install with::

    pip install -r requirements.txt

Optional Dependencies
---------------------

For building documentation::

    pip install sphinx sphinx-rtd-theme

For development::

    pip install pytest black flake8

System Requirements
-------------------

* **Memory**: Sufficient RAM to load whole slide images (typically 4GB+ recommended)
* **Storage**: Adequate disk space for output tiles and masks
* **OS**: Windows, Linux, or macOS

Note: Whole slide images can be very large (several GB), so ensure you have adequate
system resources for processing.

