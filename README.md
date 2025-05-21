# Model Viewer

Use Blender `bpy` module for 3D renderings.

## Installation

```bash
uv sync
```

## Getting Started

```bash
uv run main.py -h 

# run turntable
uv run main.py turntable --model-path path/to/obj-folder --output-dir path/to/output --config.num-frames 20
uv run main.py turntable --model-path path/to/file.obj --output-dir path/to/output --config.num-frames 20
```

Configure the coordinate system and setup the camera: 

```bash
uv run main.py turntable --model-path file.obj --output-dir output \
    --config.up "X" \
    --config.forward "Y"  \
    --config.camera-distance 2.5 \
    --config.camera-height 0.5
```
