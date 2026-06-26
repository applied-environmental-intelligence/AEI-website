# Applied Environmental Intelligence (AEI) Website

[![Build and Deploy](https://github.com/applied-environmental-intelligence/AEI-website/actions/workflows/pages.yml/badge.svg)](https://github.com/applied-environmental-intelligence/AEI-website/actions/workflows/pages.yml)

A modern, lightweight website for Applied Environmental Intelligence showcasing subsurface monitoring and wire theft detection using fiber optic networks.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/applied-environmental-intelligence/AEI-website.git
   cd AEI-website
   ```

2. **Set up Python environment**

   **Option A: Using Mamba/Conda (Recommended)**
   ```bash
   mamba env create -f environment.yml
   mamba activate aei-website
   ```

   See [docs/MAMBA_GUIDE.md](docs/MAMBA_GUIDE.md) for detailed mamba/conda instructions.

   **Option B: Using venv (no extra packages needed)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

   The build script only uses Python's standard library (`shutil`, `pathlib`) — no `pip install` step is required.

3. **Build the site**
   ```bash
   python build.py
   ```

   The build script copies all static assets from `docs/` to `dist/`. All sections of the front page depend on assets in `docs/assets/` — the hero video, capability images, team portraits, and JavaScript are all copied automatically. `build.py` handles this in one step.

4. **Preview locally**
   ```bash
   python -m http.server --directory dist 8000
   ```
   Open [http://localhost:8000](http://localhost:8000) in your browser.

   > **Important**: always serve from `dist/` via a local HTTP server. Opening `dist/index.html` directly with `file://` will block the hero video and some assets due to browser security restrictions.

## 📁 Repository Structure

```
AEI-website/
├── .github/
│   └── workflows/
│       └── pages.yml          # GitHub Actions workflow for automated deployment
├── docs/                      # Source files (edit these, never edit dist/)
│   ├── index.html             # Main HTML page
│   ├── assets/
│   │   ├── capabilities/      # Capability section images
│   │   ├── industries/        # Industry card photos
│   │   ├── js/
│   │   │   └── home.js        # Scroll-reveal and hero canvas animation
│   │   ├── portraits/         # Team portrait photos
│   │   ├── videos/
│   │   │   └── hero-loop.mp4  # Background video for the hero section
│   │   └── source/            # Build inputs — NOT copied to dist/
│   │       └── subsurface.png # Source image (kept for future use)
│   ├── CONTRIBUTING.md
│   ├── MAMBA_GUIDE.md
│   └── UPDATE_GUIDE.md
├── dist/                      # Build output (generated — do not edit!)
│   ├── index.html
│   └── assets/                # Copied from docs/assets/ (source/ excluded)
├── build.py                   # Build orchestration script
├── environment.yml            # Conda/Mamba environment specification
└── README.md
```

## 🔨 Build Process

`build.py` runs three steps:

1. **Clean** — removes and recreates `dist/`
2. **Copy** — copies `docs/index.html` and `docs/assets/` (excluding `assets/source/`) to `dist/`
3. **Validate** — checks that `dist/index.html` exists

```bash
python build.py
```

### What goes into dist/

| Asset | Source | Notes |
|---|---|---|
| `index.html` | `docs/index.html` | Main page |
| `assets/videos/hero-loop.mp4` | `docs/assets/videos/` | Hero background video |
| `assets/js/home.js` | `docs/assets/js/` | Scroll-reveal & hero canvas |
| `assets/capabilities/*.png` | `docs/assets/capabilities/` | Capability section images |
| `assets/industries/*.jpg` | `docs/assets/industries/` | Industry card photos |
| `assets/portraits/*.jpg` | `docs/assets/portraits/` | Team portraits |

`docs/assets/source/` is intentionally excluded from `dist/` — it holds build inputs, not web assets.

## 🌐 GitHub Pages Deployment

The site automatically deploys to GitHub Pages on every push to `main`.

### Asset paths

All assets use **relative paths**, so they work identically in local preview and on GitHub Pages:

```html
<img src="assets/capabilities/das-car-clean.png" />
<video src="assets/videos/hero-loop.mp4"></video>
<script src="assets/js/home.js"></script>
```

### Initial setup (one-time)

1. Go to **Settings → Pages** in your GitHub repository
2. Under **Source**, select **GitHub Actions**
3. The workflow builds and deploys on the next push

### Deployment URL

```
https://applied-environmental-intelligence.github.io/AEI-website/
```

### Manual deployment

1. Go to the **Actions** tab
2. Select "Build and Deploy to GitHub Pages"
3. Click **Run workflow**

## 📝 Updating Content

Always edit files in `docs/`, never in `dist/`.

- **Update HTML**: edit [docs/index.html](docs/index.html)
- **Add images**: place in the appropriate `docs/assets/` subdirectory and reference with a relative path
- **Add pages**: create new HTML files in `docs/` and update navigation

For detailed instructions including LinkedIn post embedding and YouTube video embedding, see [docs/UPDATE_GUIDE.md](docs/UPDATE_GUIDE.md).

## 🔧 Troubleshooting

### Sections of the page are blank or images are missing

Run `python build.py` to ensure all assets are copied to `dist/`, then serve with `python -m http.server --directory dist 8000`. Do not open `dist/index.html` directly from the filesystem (`file://`).

### Hero video does not play

The file `docs/assets/videos/hero-loop.mp4` must exist. It is committed to the repo. If missing after a shallow clone, run `git lfs pull` or re-clone with full history.

### GitHub Pages deployment fails

1. Check the **Actions** tab for error logs
2. Ensure GitHub Pages is configured to use GitHub Actions as source

## 🤝 Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

## 📦 Dependencies

The build script uses only Python's standard library — no pip packages required.

### External services
- **FormSubmit.co** — contact form handling (no backend required)
- **Google Analytics** — website analytics (ID: G-8T592QEDC5)

## 📄 License

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**

**Academic use:** ✅ Freely permitted for research, education, and non-profit purposes  
**Commercial use:** ⚠️ Requires explicit written permission from Applied Environmental Intelligence

See [LICENSE](LICENSE) for full terms.

## 📧 Contact

For questions or support, use the website's contact form or reach out to the AEI team.

---

**Built with**: Python · GitHub Actions · GitHub Pages
