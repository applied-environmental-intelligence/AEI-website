# Source Assets

This directory contains source files used to generate animation assets for the AEI website.

## Required File: subsurface.png

The `generate_reveal_subsurface.py` script requires a source PNG image named `subsurface.png` to be placed in this directory.

### Why is this file not in the repository?

This file may be:
- Too large to commit to Git efficiently
- Subject to licensing restrictions
- A proprietary or sensitive image
- Under active development and frequently updated

### How to add it

1. **Obtain the source image** (contact the AEI team or use your own subsurface monitoring image)

2. **Place it in this directory**:
   ```bash
   # Copy your image to this location
   cp /path/to/your/subsurface.png docs/assets/source/subsurface.png
   ```

3. **Verify it's in place**:
   ```bash
   ls -lh docs/assets/source/subsurface.png
   ```

4. **Build the site** to generate the reveal animation:
   ```bash
   python build.py
   ```

### Image Requirements

- **Format**: PNG (with or without transparency)
- **Size**: Any size (the animation will match the input dimensions)
- **Content**: Should be a subsurface monitoring visualization or related imagery
- **Color mode**: RGB or RGBA

### What happens if the file is missing?

- The `cable_animation.gif` will still be generated successfully
- The `subsurface_reveal.gif` generation will be skipped
- The build will complete with a warning
- The website will display correctly except for the reveal animation

### Creating a test placeholder

If you need a placeholder for testing, you can create a simple test image:

```bash
# Using ImageMagick (if installed)
convert -size 800x600 gradient:blue-cyan docs/assets/source/subsurface.png

# Or using Python
python3 << 'EOF'
from PIL import Image, ImageDraw
img = Image.new('RGB', (800, 600), (17, 34, 51))
draw = ImageDraw.Draw(img)
draw.text((400, 300), "Subsurface Placeholder", fill=(255, 255, 255), anchor="mm")
img.save('docs/assets/source/subsurface.png')
print("Created placeholder: docs/assets/source/subsurface.png")
EOF
```

### Alternative: Use Git LFS

If you want to commit the file to the repository but it's large (>5 MB), consider using [Git LFS](https://git-lfs.github.com/):

```bash
# Install Git LFS
brew install git-lfs  # macOS
# or follow instructions at https://git-lfs.github.com/

# Initialize Git LFS in your repository
git lfs install

# Track PNG files in this directory
git lfs track "docs/assets/source/*.png"

# Add the file
git add docs/assets/source/subsurface.png .gitattributes
git commit -m "Add subsurface source image with Git LFS"
```

## Questions?

See the main [README.md](../../../README.md) or [UPDATE_GUIDE.md](../../../docs/UPDATE_GUIDE.md) for more information.
