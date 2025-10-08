#!/usr/bin/env python3
"""
Convert image sequences in *_textured folders to animated GIFs.
"""

import os
import sys
import argparse
import subprocess
import glob
from pathlib import Path

# Default configuration
DEFAULT_DELAY = 10  # Delay between frames in 1/100th of a second (10 = 0.1s)
DEFAULT_LOOP = 0  # 0 = infinite loop
DEFAULT_RESIZE = "50%"  # Resize to 50% to reduce file size, or None to keep original
DEFAULT_OUTPUT_DIR = "output/texture_outs_gif"

def natural_sort_key(s):
    """Sort filenames naturally (render_2.png before render_10.png)"""
    import re
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', str(s))]

def create_gif(textured_folder, delay, loop, resize, output_base_dir=None, input_base_dir=None):
    """Create a GIF from all PNG images in the given folder."""
    folder_path = Path(textured_folder)

    # Find all PNG files and sort them naturally
    png_files = sorted(folder_path.glob("*.png"), key=natural_sort_key)

    if not png_files:
        print(f"⚠️  No PNG files found in {folder_path}")
        return False

    # Create output filename
    parent_name = folder_path.parent.name

    if output_base_dir:
        # Save to custom output directory, maintaining structure
        output_base = Path(output_base_dir)

        if input_base_dir:
            # Maintain the relative path structure from input to output
            input_base = Path(input_base_dir)
            relative_path = folder_path.parent.relative_to(input_base)
            output_dir = output_base / relative_path
        else:
            output_dir = output_base

        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{parent_name}.gif"
    else:
        # Save in parent directory (default behavior)
        output_file = folder_path.parent / f"{parent_name}.gif"

    print(f"📸 Creating GIF from {len(png_files)} images in {folder_path.name}")
    print(f"   → {output_file}")

    # Build ImageMagick command
    cmd = ["convert", "-delay", str(delay), "-loop", str(loop), "-dispose", "previous"]

    # Add all input files
    cmd.extend([str(f) for f in png_files])

    # Add resize option if specified
    if resize:
        cmd.extend(["-resize", resize])

    # Coalesce layers and optimize for proper frame handling
    cmd.extend(["-coalesce", "-layers", "optimize"])

    # Add output file
    cmd.append(str(output_file))

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        file_size = output_file.stat().st_size / (1024 * 1024)  # Size in MB
        print(f"   ✓ Created {output_file.name} ({file_size:.2f} MB)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Error creating GIF: {e.stderr.decode()}")
        return False

def main():
    """Find all *_textured folders and create GIFs."""
    parser = argparse.ArgumentParser(
        description="Convert image sequences in *_textured folders to animated GIFs"
    )
    parser.add_argument(
        "--input-dir",
        "-i",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to search for image sequences (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=None,
        help="Directory to save GIF files (default: save next to original images)"
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=DEFAULT_DELAY,
        help=f"Delay between frames in 1/100th of a second (default: {DEFAULT_DELAY})"
    )
    parser.add_argument(
        "--loop",
        type=int,
        default=DEFAULT_LOOP,
        help=f"Loop count, 0 = infinite (default: {DEFAULT_LOOP})"
    )
    parser.add_argument(
        "--resize",
        default=DEFAULT_RESIZE,
        help=f"Resize percentage or 'none' for original size (default: {DEFAULT_RESIZE})"
    )

    args = parser.parse_args()

    # Handle resize option
    resize = None if args.resize.lower() == "none" else args.resize

    input_path = Path(args.input_dir)

    if not input_path.exists():
        print(f"❌ Input directory not found: {args.input_dir}")
        return

    # Create output directory if specified
    if args.output_dir:
        output_path = Path(args.output_dir)
        if not output_path.exists():
            print(f"📁 Creating output directory: {args.output_dir}")
            output_path.mkdir(parents=True, exist_ok=True)

    # Find all *_textured folders
    textured_folders = sorted(input_path.glob("**/*_textured"))

    print(f"Found {len(textured_folders)} folders with image sequences\n")
    print(f"Input directory: {args.input_dir}")
    print(f"Output directory: {args.output_dir or 'same as input'}")
    print(f"Settings: delay={args.delay/100}s, loop={'infinite' if args.loop==0 else args.loop}, resize={resize or 'original'}\n")

    success_count = 0
    for i, folder in enumerate(textured_folders, 1):
        print(f"[{i}/{len(textured_folders)}]")
        if create_gif(folder, args.delay, args.loop, resize, args.output_dir, args.input_dir):
            success_count += 1
        print()

    print(f"✅ Successfully created {success_count}/{len(textured_folders)} GIFs")

if __name__ == "__main__":
    main()
