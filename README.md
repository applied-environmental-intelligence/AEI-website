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

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r scripts/requirements.txt
   ```

4. **Add the subsurface source image** (required for reveal animation)
   - Place your `subsurface.png` file in `src/assets/source/`
   - See [src/assets/source/README.md](src/assets/source/README.md) for details

5. **Build the site**
   ```bash
   python build.py
   ```

6. **Preview locally**
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
│   └── requirements.txt       # Python dependencies
├── dist/                      # Build output (generated, do not edit!)
│   ├── index.html            # Compiled HTML
│   └── animations/           # Generated animation assets
│       ├── cable_animation.gif
│       └── subsurface_reveal.gif
├── docs/                      # Documentation
│   ├── UPDATE_GUIDE.md       # Guide for updating content
│   └── CONTRIBUTING.md       # Contribution guidelines
├── build.py                   # Build orchestration script
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

## 🌐 GitHub Pages Deployment

The site automatically deploys to GitHub Pages on every push to the `main` branch.

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
