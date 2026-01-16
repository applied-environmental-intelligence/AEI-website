# Mamba/Conda Quick Reference

This project includes a `environment.yml` file for easy setup with mamba or conda.

## Initial Setup

```bash
# Create the environment (first time only)
mamba env create -f environment.yml

# Or using conda if you don't have mamba
conda env create -f environment.yml
```

## Daily Usage

```bash
# Activate the environment
mamba activate aei-website
# or: conda activate aei-website

# Deactivate when done
mamba deactivate
# or: conda deactivate
```

## Generate Animations

```bash
# Make sure environment is activated
mamba activate aei-website

# Generate cable animation
python scripts/generate_cable_animation.py --output dist/animations/cable_animation.gif

# Generate subsurface reveal (requires source image)
python scripts/generate_reveal_subsurface.py \
  --input src/assets/source/subsurface.png \
  --output dist/animations/subsurface_reveal.gif

# Or use the full build script
python build.py
```

## Create Placeholder Image

If you don't have a subsurface.png yet:

```bash
mamba activate aei-website
python scripts/create_placeholder.py
```

This creates a test image at `src/assets/source/subsurface.png`.

## Update Environment

If dependencies change in `environment.yml`:

```bash
# Update existing environment
mamba env update -f environment.yml --prune

# Or recreate from scratch
mamba env remove -n aei-website
mamba env create -f environment.yml
```

## Troubleshooting

### Environment activation fails

Make sure conda/mamba is initialized for your shell:

```bash
# For bash/zsh
conda init zsh
# or
mamba init zsh

# Restart your terminal after initialization
```

### Import errors

If you get "ModuleNotFoundError", ensure:
1. Environment is activated: `mamba activate aei-website`
2. Dependencies are installed: `mamba env create -f environment.yml`

### Check installed packages

```bash
mamba activate aei-website
mamba list | grep -E "pillow|numpy"
```

Should show:
- pillow: 10.0.0 or higher
- numpy: 1.24.0 or higher

## Why Mamba?

Mamba is a faster reimplementation of conda that:
- Resolves dependencies much faster
- Uses less memory
- Has a better conflict resolution algorithm
- Is a drop-in replacement for conda (same commands)

If you don't have mamba, install it:
```bash
conda install -n base -c conda-forge mamba
```

Or just use `conda` - all commands work with either!
