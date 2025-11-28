# Sphinx Documentation Setup

This document describes the Sphinx documentation setup for the Whole Slide Image Annotation Extractor project.

## What Was Created

### Documentation Files
- `docs/conf.py` - Sphinx configuration file
- `docs/index.rst` - Main documentation entry point
- `docs/overview.rst` - Project overview and architecture
- `docs/installation.rst` - Installation instructions
- `docs/usage.rst` - Usage guide and command-line interface
- `docs/api.rst` - Complete API reference documentation
- `docs/examples.rst` - Usage examples and tutorials

### Build Files
- `docs/Makefile` - Build script for Linux/macOS
- `docs/make.bat` - Build script for Windows
- `docs/README.md` - Documentation build instructions
- `docs/QUICKSTART.md` - Quick start guide

### Configuration Files
- `requirements-docs.txt` - Documentation dependencies
- `requirements.txt` - Project dependencies
- `.gitignore` - Git ignore file (includes docs build directory)

## Building the Documentation

### Step 1: Install Dependencies
```bash
pip install -r requirements-docs.txt
```

### Step 2: Build Documentation

**Windows:**
```bash
cd docs
make.bat html
```

**Linux/macOS:**
```bash
cd docs
make html
```

### Step 3: View Documentation
Open `docs/_build/html/index.html` in your web browser.

## Documentation Features

- **Auto-generated API docs** from docstrings using autodoc
- **Google/NumPy style docstrings** support via Napoleon extension
- **Read the Docs theme** for professional appearance
- **Cross-references** to Python, NumPy, OpenCV, and Shapely documentation
- **Code examples** and usage tutorials
- **Search functionality** built-in

## Publishing to GitHub Pages

1. Build the HTML documentation:
   ```bash
   cd docs
   make html  # or make.bat html on Windows
   ```

2. Option A - Using docs folder:
   - Copy contents of `docs/_build/html/` to `docs/` folder in main branch
   - Enable GitHub Pages in repository settings to serve from `/docs` folder

3. Option B - Using gh-pages branch:
   - Create a `gh-pages` branch
   - Copy contents of `docs/_build/html/` to the root of `gh-pages` branch
   - Push to GitHub

## Customization

### Changing Theme
Edit `docs/conf.py` and change:
```python
html_theme = 'sphinx_rtd_theme'
```

Other popular themes:
- `'alabaster'` (default)
- `'sphinx_rtd_theme'` (Read the Docs)
- `'bizstyle'`
- `'classic'`

### Adding New Pages
1. Create a new `.rst` file in `docs/`
2. Add it to the `toctree` in `docs/index.rst`

### Modifying API Documentation
The API documentation is auto-generated from docstrings. To modify:
1. Update docstrings in `batch_geojson_to_tiles_and_masks.py`
2. Rebuild the documentation

## Troubleshooting

### Import Errors
If you get import errors when building:
- Ensure the parent directory is in Python path (already configured in `conf.py`)
- Install all project dependencies: `pip install -r requirements.txt`

### Theme Not Found
If the Read the Docs theme is not found:
```bash
pip install sphinx-rtd-theme
```

### Build Errors
- Check that all `.rst` files are properly formatted
- Ensure all referenced files exist
- Check for syntax errors in `conf.py`

## Next Steps

1. Review and customize the documentation content
2. Add any project-specific information
3. Build and test the documentation locally
4. Set up GitHub Pages for online hosting
5. Update documentation as the code evolves

