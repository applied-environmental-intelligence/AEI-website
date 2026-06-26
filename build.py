#!/usr/bin/env python3
"""
Build script for AEI Website.

This script:
1. Cleans and creates the dist/ directory
2. Copies static assets from docs/ to dist/
3. Validates all expected outputs exist
4. Exits non-zero on failure

Usage:
    python build.py
"""
import shutil
import sys
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.resolve()
SRC_DIR = PROJECT_ROOT / "docs"
DIST_DIR = PROJECT_ROOT / "dist"


def clean_dist():
    """Remove and recreate the dist directory."""
    print("🧹 Cleaning dist/ directory...")
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)
    print("✓ dist/ directory ready")


def copy_static_assets():
    """Copy all static files from docs/ to dist/."""
    print("\n📦 Copying static assets from docs/ to dist/...")
    
    # Copy index.html
    src_html = SRC_DIR / "index.html"
    if src_html.exists():
        shutil.copy2(src_html, DIST_DIR / "index.html")
        print(f"  ✓ Copied {src_html.name}")
    else:
        print(f"  ✗ Warning: {src_html} not found", file=sys.stderr)

    # Copy nested assets used by the page (videos, images, JS)
    # Exclude assets/source/ — it holds build inputs, not web assets.
    src_assets = SRC_DIR / "assets"
    if src_assets.exists():
        shutil.copytree(
            src_assets,
            DIST_DIR / "assets",
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("source"),
        )
        print("  ✓ Copied assets/ directory")

    # Copy other top-level asset directories if they exist (future-proofing)
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

        # Step 3: Validate outputs
        outputs_ok = validate_outputs()
        
        # Final status
        print("\n" + "=" * 60)
        if outputs_ok:
            print("✓ Build completed successfully!")
            print(f"\nOutput directory: {DIST_DIR}")
            print("\nTo preview locally, run:")
            print(f"  python -m http.server --directory {DIST_DIR.relative_to(PROJECT_ROOT)} 8000")
            print("  Then open: http://localhost:8000")
            print("=" * 60)
            return 0
        else:
            print("⚠ Build completed with warnings")
            print("\nSome expected outputs are missing.")
            print("=" * 60)
            return 1
    
    except Exception as e:
        print(f"\n✗ Build failed with error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
