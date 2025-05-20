from pathlib import Path
from typing import Any, Protocol, Type


class ViewerInterface(Protocol):
    def render(self, output_path: Path) -> None: ...
    def save_blend_file(self, output_path: Path) -> None: ...
    def load_model(self, model_path: Path) -> Any: ...
    def unload_model(self, obj: Any) -> None: ...


def process(
    viewer: ViewerInterface,
    filepath: Path,
):
    obj = viewer.load_model(filepath)
    viewer.render(filepath.with_suffix(".png"))
    viewer.unload_model(obj)


def run(
    model_path: Path,
    viewer_cls: Type[ViewerInterface],
    to_blend_file: None | Path = None,
):
    viewer = viewer_cls()

    if model_path.is_file():
        process(viewer, model_path)

    else:
        file_list = model_path.glob("*.obj")
        for path in file_list:
            process(viewer, path)

    if to_blend_file is not None:
        viewer.save_blend_file(to_blend_file)

if __name__ == "__main__":

    class Dummpy:
        def render(self, output_path: Path) -> None:
            pass

        def save_blend_file(self, output_path: Path) -> None:
            pass

        def load_model(self, model_path: Path) -> Any:
            pass

        def unload_model(self, obj: Any) -> None:
            pass

    run(Path("data/"), Dummpy)
    print("finished")
