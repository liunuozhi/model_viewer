from pathlib import Path
from typing import Any

import bpy

from .presets import FollowCameraPreset
from .simple_viewer import SimpleViewer


class TurntableViewer(SimpleViewer, FollowCameraPreset):
    def __init__(
        self,
        num_frames: int = 5,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.num_frames = num_frames

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

        # Add a camera following a path.
        follow_path = self.create_follow_path()
        self.camera, self.follow_ctr = self.add_follow_camera(
            location=(0, 0, 0),
            track_target=target,
            track_path=follow_path,
        )

    def render(self, output_path: Path) -> Any:
        output_path.mkdir(parents=True, exist_ok=True)

        R = bpy.context.scene.render
        R.resolution_x = self.resolution[0]
        R.resolution_y = self.resolution[1]
        R.film_transparent = self.transparent_background
        R.image_settings.file_format = "PNG"
        R.image_settings.color_mode = "RGBA"

        bpy.context.scene.camera = self.camera

        total_frames = self.num_frames

        for i in range(total_frames):
            self.follow_ctr.offset = (
                i / total_frames * 100
            )  # percent to one circle (100%)
            file_path = output_path / f"render_{i}.png"
            R.filepath = self.path_to_str(file_path)
            bpy.ops.render.render(animation=False, write_still=True)

    def create_follow_path(
        self,
        radius: float = 3.0,
        location: tuple[float, float, float] = (0, 0, 1),
    ) -> None:
        bpy.ops.curve.primitive_bezier_circle_add(
            radius=radius,
            location=location,
        )
        return bpy.context.object


if __name__ == "__main__":
    viewer = TurntableViewer()
    viewer.load_model(Path("data/model.obj"))
    viewer.render(Path("output/model"))
    viewer.save_blend_file(Path("output/test.blend"))
    print("finished")
