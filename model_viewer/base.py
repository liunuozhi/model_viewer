import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import bpy


class BaseViewer(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.empty_scene()

    def empty_scene(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)

    def save_blend_file(self, output_path: Path, exit_after_save: bool = True) -> None:
        """Save the current blend file to the output path."""
        assert output_path.suffix == ".blend", "output_path must be a .blend file"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        bpy.ops.wm.save_mainfile(
            filepath=self.path_to_str(output_path),
            relative_remap=False,  # update assets links
            exit=exit_after_save,
        )

    @staticmethod
    def path_to_str(path: Path) -> str:
        """Convert a Path to a string."""
        return str(path.absolute())

    @abstractmethod
    def setup_scene(self) -> Any:
        """setup the 3d scene (cameras, lights, materials, etc.)."""
        ...

    @abstractmethod
    def render(self) -> Any:
        """Render the scene."""
        ...
