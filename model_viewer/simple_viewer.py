import math
from dataclasses import dataclass, field
from pathlib import Path

import bpy

from model_viewer.base_viewer import BaseViewer, BasicConfig

from .utils import move_object_to_center, scale_to_unit_cube


@dataclass
class SimpleConfig(BasicConfig):
    model_path: Path = field(default_factory=lambda: Path(""))
    camera_location: tuple[float, float, float] = (0, 3, 1)  # x, y, z


class SimpleViewer(BaseViewer[SimpleConfig]):
    def __init__(self, config: SimpleConfig):
        super().__init__(config)
        self.camera = None
        self.target = None  # look-at target
        self.render_settings = None
        self.setup_scene()

    def setup_scene(self) -> None:
        self.setup_target()
        self.setup_camera()
        self.setup_light()
        self.import_model()
        self.setup_render()

    def setup_target(self) -> None:
        """Create an empty object as a target for camera and lights."""
        bpy.ops.object.empty_add(location=(0, 0, 0))
        self.target = bpy.data.objects["Empty"]

    def setup_camera(self) -> None:
        bpy.ops.object.camera_add(location=self.config.camera_location)
        camera = bpy.data.objects["Camera"]
        # make camera look at target
        track_to = camera.constraints.new(type="TRACK_TO")
        track_to.target = self.target
        track_to.track_axis = "TRACK_NEGATIVE_Z"
        track_to.up_axis = "UP_Y"
        self.camera = camera

    def setup_light(self) -> None:
        # create two sets of lights
        # one is the sun light to have a nice shadow
        self.setup_sunlight()
        # one is 6 area lights to lower the contrast
        self.setup_arealights()

    def setup_sunlight(self) -> None:
        bpy.ops.object.light_add(type="SUN")
        sun = bpy.data.objects["Sun"]
        sun.data.energy = 5.0  # Strength

    def setup_arealights(
        self,
        num_lights: int = 6,
        radius: float = 3.5,
        height: float = 2.5,
        light_size: float = 2.0,
        light_energy: float = 25.0,
        light_color: tuple[float, float, float] = (1.0, 0.9, 0.8),
    ) -> None:
        for i in range(num_lights):
            # distribute evenly in a circle
            angle = 2.0 * math.pi * i / num_lights
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            # Add area light
            bpy.ops.object.light_add(type="AREA", location=(x, y, height))

            light = bpy.context.active_object
            light.data.shape = "RECTANGLE"
            light.data.size = light_size
            light.data.energy = light_energy
            light.data.color = light_color

            # keep light facing to the target
            track_to = light.constraints.new(type="TRACK_TO")
            track_to.target = self.target
            track_to.track_axis = "TRACK_NEGATIVE_Z"
            track_to.up_axis = "UP_Y"

    def import_model(self) -> None:
        assert self.config.model_path.suffix == ".obj"

        filepath = self.path_to_str(self.config.model_path)
        bpy.ops.wm.obj_import(filepath=filepath)
        self.logger.info(f"Imported model from {filepath}")

        imported_objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]

        assert len(imported_objects) == 1, "Expected exactly one mesh object"
        obj = imported_objects[0]
        scale_to_unit_cube(obj)
        move_object_to_center(obj)
        self.logger.info(f"Object origin: {list(obj.location)}")

    def setup_render(self, res_x: int = 1080, res_y: int = 1080) -> None:
        render_settings = bpy.context.scene.render
        render_settings = bpy.context.scene.render
        render_settings.resolution_x = res_x
        render_settings.resolution_y = res_y
        # image settings
        render_settings.film_transparent = True  # transparent background
        render_settings.image_settings.file_format = "PNG"
        render_settings.image_settings.color_mode = "RGBA"
        # output settings
        output_path = self.path_to_str(
            self.config.output_path / "render.png",
        )
        render_settings.filepath = output_path

        self.render_settings = render_settings

    def render(self) -> None:
        # set camera to active
        bpy.context.scene.camera = self.camera
        # run rendering
        bpy.ops.render.render(animation=False, write_still=True)
        self.logger.info(f"Rendered image saved to {self.config.output_path}")


if __name__ == "__main__":
    config = SimpleConfig(model_path=Path("./data/model.obj"))
    viewer = SimpleViewer(config)
    viewer.render()
    # viewer.save_blend_file()
