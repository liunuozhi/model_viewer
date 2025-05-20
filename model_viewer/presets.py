import math

import bpy


class SunLightPreset:
    def add_sunlight(self, energy: float = 5.0):
        bpy.ops.object.light_add(type="SUN")
        sun = bpy.context.object

        sun.data.energy = energy
        return sun


class AreaLightPreset:
    def add_arealight(
        self,
        location: tuple[float, float, float],
        energy: float = 5.0,
        light_size: float = 2.0,
        light_color: tuple[float, float, float] = (1.0, 0.9, 0.8),
        track_target: bpy.types.Object | None = None,
    ):
        bpy.ops.object.light_add(type="AREA", location=location)
        light = bpy.context.object

        light.data.energy = energy
        light.data.size = light_size
        light.data.color = light_color

        if track_target is not None:
            track_to = light.constraints.new(type="TRACK_TO")
            track_to.target = track_target
            track_to.track_axis = "TRACK_NEGATIVE_Z"
            track_to.up_axis = "UP_Y"

        return light


class ManyAreaLightsPreset(AreaLightPreset):
    def add_many_arealights(
        self,
        num_lights: int = 6,
        radius: float = 3.5,
        height: float = 2.5,
        energy: float = 25.0,
        light_size: float = 2.0,
        light_color: tuple[float, float, float] = (1.0, 0.9, 0.8),
        track_target: bpy.types.Object | None = None,
    ):
        for i in range(num_lights):
            angle = 2.0 * math.pi * i / num_lights
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            self.add_arealight(
                location=(x, y, height),
                energy=energy,
                light_size=light_size,
                light_color=light_color,
                track_target=track_target,
            )


class TrackTargetPreset:
    def add_track_target(
        self,
        location: tuple[float, float, float] = (0, 0, 0),
    ):
        bpy.ops.object.empty_add(location=location)
        return bpy.context.object


class CameraPreset:
    def add_camera(
        self,
        location: tuple[float, float, float] = (0, 0, 0),
        track_target: bpy.types.Object | None = None,
    ):
        bpy.ops.object.camera_add(location=location)
        camera = bpy.context.object

        if track_target is not None:
            track_to = camera.constraints.new(type="TRACK_TO")
            track_to.target = track_target
            track_to.track_axis = "TRACK_NEGATIVE_Z"
            track_to.up_axis = "UP_Y"

        return camera

class FollowCameraPreset:
    def add_follow_camera(
        self,
        location: tuple[float, float, float] = (0, 0, 0),
        track_target: bpy.types.Object | None = None,
        track_path: bpy.types.Object | None = None,
    ):
        bpy.ops.object.camera_add(location=location)
        camera = bpy.context.object

        if track_path is not None:
            follow_ctr = camera.constraints.new(type="FOLLOW_PATH")
            follow_ctr.target = track_path

        if track_target is not None:
            track_to = camera.constraints.new(type="TRACK_TO")
            track_to.target = track_target
            track_to.track_axis = "TRACK_NEGATIVE_Z"
            track_to.up_axis = "UP_Y"

        return camera, follow_ctr
