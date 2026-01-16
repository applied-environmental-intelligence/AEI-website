#!/usr/bin/env python3
"""
Build script for AEI Website.

This script:
1. Cleans and creates the dist/ directory
2. Copies static assets from src/ to dist/
3. Generates animation assets using Python scripts
4. Validates all outputs exist
5. Exits non-zero on failure

Usage:
    python build.py
"""
import shutil import subprocess
import sys
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.resolve()
SRC_DIR = PROJECT_ROOT / "src"
DIST_DIR = PROJECT_ROOT / "dist"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
ANIMATIONS_DIR = DIST_DIR / "animations"

# Source assets
SUBSURFACE_SOURCE = SRC_DIR / "assets" / "source" / "subsurface.png"

# Expected outputs
EXPECTED_ANIMATIONS = [
    ANIMATIONS_DIR / "cable_animation.gif",
    ANIMATIONS_DIR / "subsurface_reveal.gif",
]


def clean_dist():
    """Remove and recreate the dist directory."""
    print("🧹 Cleaning dist/ directory...")
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)
    ANIMATIONS_DIR.mkdir(parents=True)
    print("✓ dist/ directory ready")


def copy_static_assets():
    """Copy all static files from src/ to dist/."""
    print("\n📦 Copying static assets from src/ to dist/...")
    
    # Copy index.html
    src_html = SRC_DIR / "index.html"
    if src_html.exists():
        shutil.copy2(src_html, DIST_DIR / "index.html")
        print(f"  ✓ Copied {src_html.name}")
    else:
        print(f"  ✗ Warning: {src_html} not found", file=sys.stderr)
    
    # Copy other assets if they exist (future-proofing)
    for item in ["css", "js", "images", "fonts"]:
        src_item = SRC_DIR / item
        if src_item.exists():
            if src_item.is_dir():
                shutil.copytree(src_item, DIST_DIR / item, dirs_exist_ok=True)
                print(f"  ✓ Copied {item}/ directory")
            else:
                shutil.copy2(src_item, DIST_DIR / item)
                print(f"  ✓ Copied {item}")
    
    print("✓ Static assets copied")


def generate_animations():
    """Run Python scripts to generate animation assets."""
    print("\n🎬 Generating animation assets...")
    
    # Generate cable animation
    print("  → Generating cable animation...")
    cable_output = ANIMATIONS_DIR / "cable_animation.gif"
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "generate_cable_animation.py"),
                "--output",
                str(cable_output),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(f"    {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Cable animation generation failed:", file=sys.stderr)
        print(f"    {e.stderr}", file=sys.stderr)
        return False
    
    # Generate subsurface reveal animation
    print("  → Generating subsurface reveal animation...")
    reveal_output = ANIMATIONS_DIR / "subsurface_reveal.gif"
    
    # Check if source image exists
    if not SUBSURFACE_SOURCE.exists():
        print(
            f"  ✗ Warning: Source file not found: {SUBSURFACE_SOURCE}",
            file=sys.stderr,
        )
        print(
            f"    Skipping subsurface reveal animation generation.",
            file=sys.stderr,
        )
        print(
            f"    See {SRC_DIR / 'assets' / 'source' / 'README.md'} for details.",
            file=sys.stderr,
        )
        # Create a placeholder note in dist
        placeholder = ANIMATIONS_DIR / "subsurface_reveal.gif.missing"
        placeholder.write_text(
            f"Source file {SUBSURFACE_SOURCE} not found. "
            "Please add it to generate this animation."
        )
        return False
    
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "generate_reveal_subsurface.py"),
                "--input",
                str(SUBSURFACE_SOURCE),
                "--output",
                str(reveal_output),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(f"    {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Subsurface reveal generation failed:", file=sys.stderr)
        print(f"    {e.stderr}", file=sys.stderr)
        return False
    
    print("✓ Animation assets generated")
    return True


def validate_outputs():
    """Verify all expected outputs exist."""
    print("\n🔍 Validating build outputs...")
    
    all_valid = True
    
    # Check index.html
    index_html = DIST_DIR / "index.html"
    if index_html.exists():
        print(f"  ✓ {index_html.relative_to(PROJECT_ROOT)}")
    else:
        print(f"  ✗ Missing: {index_html.relative_to(PROJECT_ROOT)}", file=sys.stderr)
        all_valid = False
    
    # Check animations
    for anim in EXPECTED_ANIMATIONS:
        if anim.exists():
            size_mb = anim.stat().st_size / (1024 * 1024)
            print(f"  ✓ {anim.relative_to(PROJECT_ROOT)} ({size_mb:.2f} MB)")
        else:
            print(f"  ✗ Missing: {anim.relative_to(PROJECT_ROOT)}", file=sys.stderr)
            all_valid = False
    
    if all_valid:
        print("✓ All expected outputs present")
    else:
        print("✗ Build validation failed - some outputs missing", file=sys.stderr)
    
    return all_valid


def main():
    """Main build orchestration."""
    print("=" * 60)
    print("AEI Website Build Script")
    print("=" * 60)
    
    try:
        # Step 1: Clean dist/
        clean_dist()
        
        # Step 2: Copy static assets
        copy_static_assets()
        
        # Step 3: Generate animations
        animations_ok = generate_animations()
        
        # Step 4: Validate outputs
        outputs_ok = validate_outputs()
        
        # Final status
        print("\n" + "=" * 60)
        if animations_ok and outputs_ok:
            print("✓ Build completed successfully!")
            print(f"\nOutput directory: {DIST_DIR}")
            print("\nTo preview locally, run:")
            print(f"  python -m http.server --directory {DIST_DIR.relative_to(PROJECT_ROOT)} 8000")
            print("  Then open: http://localhost:8000")
            print("=" * 60)
            return 0
        else:
            print("⚠ Build completed with warnings")
            print("\nSome animation assets could not be generated.")
            print("The site may not display correctly without all assets.")
            print("=" * 60)
            return 1
    
    except Exception as e:
        print(f"\n✗ Build failed with error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
