# Connecting to Read the Docs

This guide will help you connect your GitHub repository to Read the Docs for automatic documentation hosting.

## Prerequisites

1. A GitHub account
2. Your repository pushed to GitHub
3. A Read the Docs account (free at https://readthedocs.org)

## Step-by-Step Instructions

### Step 1: Push Your Repository to GitHub

Make sure your repository is on GitHub with all the documentation files:

```bash
git add .
git commit -m "Add Sphinx documentation"
git push origin main
```

### Step 2: Sign Up for Read the Docs

1. Go to https://readthedocs.org
2. Click "Sign Up" or "Log in"
3. Sign up using your GitHub account (recommended for easier integration)

### Step 3: Import Your Project

1. After logging in, click **"Import a Project"** or go to https://readthedocs.org/dashboard/import/
2. Click **"Import Manually"** or **"Import from GitHub"** (if you connected your GitHub account)
3. Fill in the project details:
   - **Name**: `whole-slide-image-annotation-extractor` (or your preferred name)
   - **Repository URL**: `https://github.com/yourusername/Driven_paper.git`
   - **Repository type**: Git
   - **Default branch**: `main` (or `master` if that's your default branch)
   - **Language**: Python
   - **Python configuration file**: `.readthedocs.yaml` (should be auto-detected)
4. Click **"Create"**

### Step 4: Configure Build Settings

Read the Docs should automatically detect the `.readthedocs.yaml` file. If not:

1. Go to your project settings: https://readthedocs.org/dashboard/your-project-name/edit/
2. Under **"Configuration file"**, ensure it shows: `.readthedocs.yaml`
3. Under **"Python configuration"**:
   - **Python version**: 3.9 (or as specified in `.readthedocs.yaml`)
   - **Install Project**: No (since this is a documentation-only project)
   - **Requirements file**: `requirements-docs.txt`

### Step 5: Trigger Your First Build

1. Go to your project dashboard: https://readthedocs.org/dashboard/your-project-name/
2. Click **"Build version"** or **"Build latest"**
3. Wait for the build to complete (usually 2-5 minutes)
4. Check the build log for any errors

### Step 6: Access Your Documentation

Once the build succeeds, your documentation will be available at:
```
https://your-project-name.readthedocs.io/
```

## Configuration Files

### `.readthedocs.yaml`

This file tells Read the Docs how to build your documentation:

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.9"

sphinx:
  configuration: docs/conf.py

python:
  install:
    - requirements: requirements.txt
    - requirements: requirements-docs.txt
```

### `requirements-docs.txt`

Contains documentation dependencies:
```
sphinx>=4.0.0
sphinx-rtd-theme>=1.0.0
```

## Troubleshooting

### Build Fails with Import Errors

If you see errors about missing modules (like `shapely`, `numpy`, etc.):

1. **Option 1**: Add them to `requirements-docs.txt` (even if not needed for docs):
   ```
   sphinx>=4.0.0
   sphinx-rtd-theme>=1.0.0
   numpy>=1.20.0
   shapely>=1.8.0
   ```

2. **Option 2**: Configure autodoc to skip imports in `docs/conf.py`:
   ```python
   autodoc_mock_imports = ['shapely', 'cv2', 'tifffile', 'pandas']
   ```

### Build Fails with Path Errors

If you see path-related errors, ensure `docs/conf.py` has:
```python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

### Theme Not Found

The `sphinx-rtd-theme` should be installed via `requirements-docs.txt`. If not:
1. Ensure `requirements-docs.txt` includes `sphinx-rtd-theme>=1.0.0`
2. Rebuild the documentation

## Automatic Builds

Read the Docs automatically rebuilds your documentation when you:
- Push commits to your default branch
- Create or update tags/releases
- Manually trigger a build from the dashboard

## Custom Domain (Optional)

You can use a custom domain:
1. Go to project settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

## Version Management

Read the Docs automatically:
- Builds documentation for all Git tags
- Creates versions for branches (if enabled)
- Maintains a "latest" version pointing to your default branch

## Updating Documentation

Simply push changes to GitHub:
```bash
git add .
git commit -m "Update documentation"
git push origin main
```

Read the Docs will automatically detect the changes and rebuild (usually within a few minutes).

## Additional Resources

- Read the Docs Documentation: https://docs.readthedocs.io/
- Sphinx Documentation: https://www.sphinx-doc.org/
- Read the Docs Support: https://readthedocs.org/support/

