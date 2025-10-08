# Model Viewer

Use Blender `bpy` module for 3D renderings.

## Installation

```bash
uv sync
```

## Getting Started

```bash
uv run main.py -h 

# Simple rendering (single image)
uv run main.py simple --model-path path/to/file.obj --output-dir output

# Turntable rendering (animated sequence)
uv run main.py turntable --model-path path/to/obj-folder --output-dir path/to/output --config.num-frames 20
uv run main.py turntable --model-path path/to/file.obj --output-dir path/to/output --config.num-frames 20
```

Configure the coordinate system and setup the camera: 

```bash
uv run main.py turntable --model-path file.obj --output-dir output \
    --config.up "X" \
    --config.forward "Y" \
    --config.camera-distance 2.5 \
    --config.camera-height 0.5
```

Configure material application:

```bash
# Apply default material (default behavior)
uv run main.py simple --model-path file.obj --output-dir output --config.apply-default-material

# Skip default material application
uv run main.py simple --model-path file.obj --output-dir output --config.no-apply-default-material
```

## Creating GIFs from Image Sequences

```bash
python3 scripts/create_gifs.py -i output/texture_outs -o output/gifs
```
