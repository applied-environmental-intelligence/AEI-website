#!/usr/bin/env python3
"""
Create a placeholder subsurface.png for testing the reveal animation.
This generates a simple gradient image that can be used for testing purposes.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def create_placeholder():
    """Create a placeholder subsurface image."""
    # Output path
    output = Path("docs/assets/source/subsurface.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    
    # Create a nice gradient image
    width, height = 1200, 800
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Create a vertical gradient from dark blue to cyan
    for y in range(height):
        # Gradient from dark blue (#112244) to cyan (#00aacc)
        r = int(0x11 + (0x00 - 0x11) * y / height)
        g = int(0x22 + (0xaa - 0x22) * y / height)
        b = int(0x44 + (0xcc - 0x44) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add some horizontal "layers" to simulate subsurface strata
    for i in range(5):
        y = int(height * (0.2 + i * 0.15))
        thickness = 2 + i
        # Darker lines
        draw.line([(0, y), (width, y)], fill=(20, 30, 50), width=thickness)
    
    # Add text label
    try:
        # Try to use a larger font if available
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    except:
        font = ImageFont.load_default()
    
    text = "PLACEHOLDER SUBSURFACE IMAGE"
    # Get text bbox
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Draw text with shadow
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Shadow
    draw.text((x + 2, y + 2), text, fill=(0, 0, 0, 128), font=font)
    # Main text
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    # Save
    img.save(output)
    print(f"✓ Created placeholder image: {output}")
    print(f"  Size: {width}×{height} pixels")
    print(f"\nYou can now run:")
    print(f"  python build.py")
    print(f"\nReplace this with your actual subsurface monitoring image when available.")

if __name__ == "__main__":
    create_placeholder()
