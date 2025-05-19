"""
blender --background --python main.py
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path so we can import model_viewer
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import package
from model_viewer.simple_viewer import SimpleConfig, SimpleViewer

if __name__ == "__main__":
    config = SimpleConfig(model_path=Path("./data/model.obj"))
    viewer = SimpleViewer(config)
    viewer.render()

    # Make sure Blender exits after rendering
    import bpy

    bpy.ops.wm.quit_blender()
