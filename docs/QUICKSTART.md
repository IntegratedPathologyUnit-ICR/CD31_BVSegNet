# Quick Start Guide for Building Documentation

## Prerequisites

1. Install Python dependencies:
   ```bash
   pip install -r ../requirements-docs.txt
   ```

## Building Documentation

### Windows
```bash
make.bat html
```

### Linux/macOS
```bash
make html
```

### View Documentation
After building, open `_build/html/index.html` in your web browser.

## Documentation Structure

* `index.rst` - Main entry point
* `overview.rst` - Project overview
* `installation.rst` - Installation guide
* `usage.rst` - Usage instructions
* `api.rst` - API reference
* `examples.rst` - Usage examples

## Publishing to GitHub Pages

1. Build the HTML: `make html` or `make.bat html`
2. Copy `_build/html/*` to your `gh-pages` branch or `docs/` folder
3. GitHub will automatically serve the documentation

