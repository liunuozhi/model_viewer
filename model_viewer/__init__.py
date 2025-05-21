from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Protocol, Type

from .simple_viewer import SimpleViewer
from .turntable_viewer import TurntableViewer


class ViewerInterface(Protocol):
    def render(self, output_path: Path) -> None: ...
    def save_blend_file(self, output_path: Path) -> None: ...
    def load_model(self, model_path: Path) -> Any: ...
    def unload_model(self, obj: Any) -> None: ...


def process(
    viewer: ViewerInterface,
    model_path: Path,
    output_dir: Path,
):
    obj = viewer.load_model(model_path)
    viewer.render(output_dir)
    viewer.unload_model(obj)


def _run(
    model_path: Path,
    output_dir: Path,
    save_to_blend: bool,
    viewer_cls: Type[ViewerInterface],
    **cls_kwargs: Any,
):
    viewer = viewer_cls(**cls_kwargs)

    if model_path.is_file():
        process(viewer, model_path, output_dir)
    else:
        file_list = model_path.glob("*.obj")
        for path in file_list:
            # for each model, create a new output directory
            model_output_dir = output_dir / path.stem
            process(viewer, path, model_output_dir)

    if save_to_blend:
        viewer.save_blend_file(output_dir / "model.blend")


@dataclass
class SimpleConfig:
    """Configuration for the simple viewer."""

    width: int = 1080
    """Width of the rendered image."""
    height: int = 1080
    """Height of the rendered image."""
    transparent_background: bool = True
    """Whether to use a transparent background."""
    up: str = "Z"
    """Up axis of the imported model."""
    forward: str = "Y"
    """Forward axis of the imported model."""


def run_simple(
    model_path: Path,
    output_dir: Path,
    config: SimpleConfig,
    save_to_blend: bool = True,
):
    _run(model_path, output_dir, save_to_blend, SimpleViewer, **asdict(config))


@dataclass
class TurntableConfig(SimpleConfig):
    """Configuration for the turntable viewer."""

    num_frames: int = 5


def run_turntable(
    model_path: Path,
    output_dir: Path,
    config: TurntableConfig,
    save_to_blend: bool = True,
):
    _run(model_path, output_dir, save_to_blend, TurntableViewer, **asdict(config))


default_dict = {
    "turntable": run_turntable,
    "simple": run_simple,
}
