# Applied Environmental Intelligence (AEI) Website

[![Build and Deploy](https://github.com/marinedenolle/AEI-website/actions/workflows/pages.yml/badge.svg)](https://github.com/marinedenolle/AEI-website/actions/workflows/pages.yml)

A modern, lightweight website for Applied Environmental Intelligence showcasing subsurface monitoring and wire theft detection using fiber optic networks.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/marinedenolle/AEI-website.git
   cd AEI-website
   ```

2. **Set up Python environment**

   **Option A: Using Mamba/Conda (Recommended)**
   ```bash
   # Create environment from environment.yml
   mamba env create -f environment.yml
   
   # Activate the environment
   mamba activate aei-website
   ```
   
   See [docs/MAMBA_GUIDE.md](docs/MAMBA_GUIDE.md) for detailed mamba/conda instructions.

   **Option B: Using venv + pip**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r scripts/requirements.txt
   ```

3. **Add the subsurface source image** (required for reveal animation)
   
   **Option A: Use your own image**
   - Place your `subsurface.png` file in `src/assets/source/`
   
   **Option B: Create a test placeholder**
   ```bash
   python scripts/create_placeholder.py
   ```
   
   See [src/assets/source/README.md](src/assets/source/README.md) for more details.

4. **Build the site**
   ```bash
   python build.py
   ```

5. **Preview locally**
   ```bash
   python -m http.server --directory dist 8000
   ```
   Open [http://localhost:8000](http://localhost:8000) in your browser

## 📁 Repository Structure

```
AEI-website/
├── .github/
│   └── workflows/
│       └── pages.yml          # GitHub Actions workflow for automated deployment
├── src/                       # Source files (edit these)
│   ├── index.html            # Main HTML page
│   └── assets/
│       └── source/
│           ├── README.md      # Instructions for source assets
│           └── subsurface.png # Source image for reveal animation (add this!)
├── scripts/                   # Build scripts
│   ├── generate_cable_animation.py
│   ├── generate_reveal_subsurface.py
│   └── requirements.txt       # Python dependencies (pip)
├── dist/                      # Build output (generated, do not edit!)
│   ├── index.html            # Compiled HTML
│   └── animations/           # Generated animation assets
│       ├── cable_animation.gif
│       └── subsurface_reveal.gif
├── docs/                      # Documentation
│   ├── UPDATE_GUIDE.md       # Guide for updating content
│   └── CONTRIBUTING.md       # Contribution guidelines
├── build.py                   # Build orchestration script
├── environment.yml            # Conda/Mamba environment specification
├── .gitignore
└── README.md                  # This file
```

## 🔨 Build Process

The build script (`build.py`) performs the following steps:

1. **Clean**: Removes and recreates `dist/` directory
2. **Copy**: Copies static assets from `src/` to `dist/`
3. **Generate**: Runs Python scripts to create animation GIFs
4. **Validate**: Checks that all expected outputs exist

### Build Commands

```bash
# Standard build
python build.py

# Build with custom Python
python3.11 build.py
```

### Build Output

- ✅ `dist/index.html` - Main page with relative asset paths
- ✅ `dist/animations/cable_animation.gif` - 3D cable wireframe animation (~4s, 1920×1080)
- ✅ `dist/animations/subsurface_reveal.gif` - Semi-circular wipe reveal (~2s, variable size)

## � Generating Animations Directly

You can run the animation scripts directly in the repository without doing a full build. This is useful for testing animation changes or generating GIFs for other purposes.

### Generate Cable Animation

```bash
# Activate your environment first
mamba activate aei-website  # or: source venv/bin/activate

# Generate in current directory (default)
python scripts/generate_cable_animation.py

# Or specify custom output location
python scripts/generate_cable_animation.py --output path/to/cable_animation.gif
```

This creates `cable_animation.gif` in the specified location (~2-4 MB, 1920×1080px, ~4 seconds).

### Generate Subsurface Reveal Animation

```bash
# First, make sure you have the source image
# Place your PNG in: src/assets/source/subsurface.png
# (See src/assets/source/README.md for details)

# Generate with default paths
python scripts/generate_reveal_subsurface.py \
  --input src/assets/source/subsurface.png \
  --output subsurface_reveal.gif

# Or generate directly to dist/animations/
python scripts/generate_reveal_subsurface.py \
  --input src/assets/source/subsurface.png \
  --output dist/animations/subsurface_reveal.gif
```

### Quick Test: Generate Both Animations

```bash
# Activate environment
mamba activate aei-website  # or: source venv/bin/activate

# Create output directory
mkdir -p test_animations

# Generate cable animation
python scripts/generate_cable_animation.py --output test_animations/cable.gif

# Generate subsurface reveal (if you have the source image)
python scripts/generate_reveal_subsurface.py \
  --input src/assets/source/subsurface.png \
  --output test_animations/reveal.gif

# View the results
ls -lh test_animations/
```

### Animation Parameters

Both scripts use hardcoded parameters for consistency. To modify:

**Cable Animation** (`scripts/generate_cable_animation.py`):
- Resolution: 1920×1080 (line 40: `W, H = 1920*2, 1080*2`)
- Duration: 4 seconds (line 44: `duration_s = 4.0`)
- Frame rate: 40 fps (line 43: `fps = 40`)
- Colors: Light gray on dark gray (lines 170-171)

**Subsurface Reveal** (`scripts/generate_reveal_subsurface.py`):
- Resolution: Matches input PNG
- Duration: 1.9 seconds (line 47: `duration_s = 1.9`)
- Frame rate: 50 fps (line 46: `fps = 50`)
- Background: `#111111` (line 10: `BG_RGBA`)

After modifying parameters, rebuild the site to update deployed animations:
```bash
python build.py
```

## �🌐 GitHub Pages Deployment

The site automatically deploys to GitHub Pages on every push to the `main` branch.
### Asset Paths and URLs

The HTML uses **relative paths** for all animations and assets:
```html
<!-- In src/index.html -->
<img src="animations/cable_animation.gif" />
<img src="animations/subsurface_reveal.gif" />
```

These relative paths work correctly in both contexts:
- **Local preview**: `http://localhost:8000/animations/cable_animation.gif`
- **GitHub Pages**: `https://marinedenolle.github.io/AEI-website/animations/cable_animation.gif`

No path changes are needed when deploying - the build process handles everything automatically!
### Initial Setup (One-Time)

1. Go to **Settings** → **Pages** in your GitHub repository
2. Under **Source**, select **GitHub Actions**
3. The workflow will automatically build and deploy on the next push

### Deployment URL

Your site will be available at:
```
https://marinedenolle.github.io/AEI-website/
```

### Manual Deployment

You can also trigger a deployment manually:
1. Go to **Actions** tab in GitHub
2. Select "Build and Deploy to GitHub Pages"
3. Click **Run workflow**

## 📝 Updating Content

**Important**: Always edit files in `src/`, never in `dist/`!

- **Update HTML**: Edit [src/index.html](src/index.html)
- **Add new pages**: Create new HTML files in `src/` and update navigation
- **Regenerate animations**: Modify scripts in `scripts/` and rebuild
- **Add images**: Place in `src/assets/` and reference with relative paths

For detailed instructions, see [docs/UPDATE_GUIDE.md](docs/UPDATE_GUIDE.md).

## 🤝 Contributing

Contributions are welcome! Please read [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📦 Dependencies

### Python Packages (scripts/requirements.txt)
- **Pillow** (≥10.0.0) - Image processing and GIF generation
- **NumPy** (≥1.24.0) - Numerical computations for 3D projections

### External Services
- **FormSubmit.co** - Contact form handling (no backend required)
- **Google Analytics** - Website analytics (ID: G-8T592QEDC5)

## 🔧 Troubleshooting

### Build fails with "subsurface.png not found"

Add the source image to `src/assets/source/subsurface.png`. See [src/assets/source/README.md](src/assets/source/README.md).

### Animations don't appear on the site

1. Check that both GIF files exist in `dist/animations/`
2. Verify paths in `src/index.html` use relative URLs: `animations/filename.gif`
3. Clear browser cache and hard reload (Ctrl+Shift+R / Cmd+Shift+R)

### GitHub Pages deployment fails

1. Check the **Actions** tab for error logs
2. Ensure GitHub Pages is configured to use GitHub Actions as source
3. Verify `scripts/requirements.txt` lists all Python dependencies

## 📄 License

Copyright © 2025 Applied Environmental Intelligence. All rights reserved.

## 📧 Contact

For questions or support, visit the website's contact form or reach out to the AEI team.

---

**Built with**: Python • Pillow • NumPy • GitHub Actions • GitHub Pages
