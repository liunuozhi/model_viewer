import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar

import bpy


@dataclass
class BasicConfig:
    output_path: Path = Path("./output")

    def __post_init__(self) -> None:
        self.output_path.mkdir(parents=True, exist_ok=True)


ConfigType = TypeVar("ConfigType", bound=BasicConfig)


class BaseViewer(ABC, Generic[ConfigType]):
    def __init__(self, config: ConfigType):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.create_empty_scene()

    @abstractmethod
    def setup_scene(self) -> None:
        """Setup the 3D scene (cameras, lights, materials, etc.)."""
        ...

    @abstractmethod
    def render(self) -> None:
        """Render the scene."""
        ...

    def create_empty_scene(self) -> None:
        """Init blender with an empty template scene."""
        bpy.ops.wm.read_factory_settings(use_empty=True)

    @staticmethod
    def path_to_str(path: Path) -> str:
        """Convert a Path to a string."""
        return str(path.absolute())

    def save_blend_file(self) -> None:
        """Save the current blend file to the output path."""
        output_path = self.path_to_str(
            self.config.output_path / "model.blend",
        )

        bpy.ops.wm.save_mainfile(
            filepath=output_path,
            relative_remap=False,  # update assets links
            exit=True,  # exit Blender after saving
        )
