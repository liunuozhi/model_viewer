from pathlib import Path
from typing import Any

import bpy

from .base import BaseViewer
from .presets import (
    CameraPreset,
    ManyAreaLightsPreset,
    SunLightPreset,
    TrackTargetPreset,
)
from .utils import move_object_to_center, scale_to_unit_cube


class SimpleViewer(
    BaseViewer,
    SunLightPreset,
    TrackTargetPreset,
    CameraPreset,
    ManyAreaLightsPreset,
):
    def __init__(self):
        super().__init__()
        self.camera = None
        self.setup_scene()

    def setup_scene(self) -> Any:
        # This target is for a look-at point.
        target = self.add_track_target()

        self.add_sunlight(energy=5.0)
        # To lower the contrast, we add 6 area lights.
        self.add_many_arealights(
            num_lights=6,
            radius=3.5,
            height=1.5,
            track_target=target,
        )
        # Add a camera.
        self.camera = self.add_camera(
            location=(0, 3, 1),
            track_target=target,
        )

    def load_model(self, model_path: Path) -> Any:
        assert model_path.suffix == ".obj"
        filepath = self.path_to_str(model_path)
        bpy.ops.wm.obj_import(filepath=filepath)

        obj = bpy.context.object
        scale_to_unit_cube(obj)
        move_object_to_center(obj)
        return obj

    def unload_model(self, obj: bpy.types.Object) -> Any:
        bpy.data.objects.remove(obj, do_unlink=True)

    def render(self, output_path: Path) -> Any:
        R = bpy.context.scene.render
        R.resolution_x = 1080
        R.resolution_y = 1080
        R.film_transparent = True
        R.image_settings.file_format = "PNG"
        R.image_settings.color_mode = "RGBA"
        R.filepath = self.path_to_str(output_path)

        bpy.context.scene.camera = self.camera
        bpy.ops.render.render(animation=False, write_still=True)


if __name__ == "__main__":
    viewer = SimpleViewer()
    obj = viewer.load_model(Path("data/model.obj"))
    viewer.render(Path("output/test.png"))
    # viewer.unload_model(obj)

    viewer.save_blend_file(Path("output/test.blend"))
    print("finished")
