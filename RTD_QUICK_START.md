# Read the Docs Quick Start

## 5-Minute Setup Guide

### 1. Push to GitHub
```bash
git add .
git commit -m "Add documentation"
git push origin main
```

### 2. Sign Up
- Go to https://readthedocs.org
- Sign up with GitHub (recommended)

### 3. Import Project
- Click "Import a Project"
- Select your repository: `yourusername/Driven_paper`
- Project name: `whole-slide-image-annotation-extractor` (or your choice)
- Click "Create"

### 4. Build
- Read the Docs will automatically detect `.readthedocs.yaml`
- Click "Build version" to trigger first build
- Wait 2-5 minutes

### 5. Access
Your docs will be live at:
```
https://your-project-name.readthedocs.io/
```

## Files Already Created

✅ `.readthedocs.yaml` - Read the Docs configuration  
✅ `requirements-docs.txt` - Documentation dependencies  
✅ `docs/conf.py` - Sphinx configuration (RTD-compatible)  
✅ All documentation source files in `docs/`

## Troubleshooting

**Build fails?** Check the build log in Read the Docs dashboard for specific errors.

**Import errors?** Uncomment the `autodoc_mock_imports` line in `docs/conf.py` if needed.

**Need help?** See [README_RTD.md](README_RTD.md) for detailed instructions.

