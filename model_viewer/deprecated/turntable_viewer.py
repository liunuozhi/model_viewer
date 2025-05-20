from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import bpy

from .simple_viewer import SimpleConfig, SimpleViewer


@dataclass
class TurntableConfig(SimpleConfig):
    total_frames: int = 20
    path_radius: float = 3.0
    path_height: float = 1.0
    camera_location: tuple[float, float, float] = (0, 0, 0)
    camera_type: Literal["ORTHO", "PERSP"] = "ORTHO"
    ortho_scale: float | None = 2.0


class TurntableViewer(SimpleViewer):
    def __init__(self, config: TurntableConfig):
        super().__init__(config)

        self.config = config
        self.follow_path = None

    def setup_camera(self) -> None:
        camera_type = self.config.camera_type
        ortho_scale = self.config.ortho_scale

        bpy.ops.object.camera_add(location=self.config.camera_location)
        camera = bpy.data.objects["Camera"]
        camera.data.type = camera_type

        if camera_type == "ORTHO" and ortho_scale is not None:
            camera.data.ortho_scale = ortho_scale

        # 1. Create camera follow path
        self.create_follow_path()
        follow_ctr = camera.constraints.new(type="FOLLOW_PATH")
        follow_ctr.target = self.follow_path

        # 2. Make camera look at target
        track_to = camera.constraints.new(type="TRACK_TO")
        track_to.target = self.target
        track_to.track_axis = "TRACK_NEGATIVE_Z"
        track_to.up_axis = "UP_Y"

        self.camera = camera
        self.follow_ctr = camera.constraints["Follow Path"]

    def create_follow_path(self) -> None:
        bpy.ops.curve.primitive_bezier_circle_add(
            radius=3.0,
            location=(0, 0, 1),
        )
        self.follow_path = bpy.context.object

    def render(self) -> None:
        camera = self.camera
        bpy.context.scene.camera = camera

        follow_ctr = self.follow_ctr
        render_settings = self.render_settings

        total_frames = self.config.total_frames

        for i in range(total_frames):
            follow_ctr.offset = i / total_frames * 100  # percent to one circle (100%)
            output_path = self.config.output_path / f"render_{i}.png"
            render_settings.filepath = self.path_to_str(output_path)
            bpy.ops.render.render(animation=False, write_still=True)


if __name__ == "__main__":
    config = TurntableConfig(
        model_path=Path("./data/model.obj"),
        camera_location=(0, 0, 0),  # require for path constraint
    )
    viewer = TurntableViewer(config)
    viewer.render()
