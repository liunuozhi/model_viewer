from pathlib import Path

import bpy


class SimpleScene:
    def __init__(
        self,
        model_path: Path,
        output_path:Path,
    ):
        self.model_path = model_path

        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path = output_path

        self.setup_scene()
        self.save_blend_file()

    def setup_scene(self):
        # create an empty collection
        bpy.ops.wm.read_factory_settings(use_empty=True)

        # load the model
        model_path = self.path_to_str(self.model_path)
        bpy.ops.wm.obj_import(filepath=model_path)

        # create a camera

        # create a sun light
        

    def save_blend_file(self):
        # bpy requires full path in str
        output_path = self.path_to_str(self.output_path)

        bpy.ops.wm.save_mainfile(
            filepath=output_path,
            relative_remap=False,  # update assets links
            exit=False,  # do not exit Blender after saving
        )
    
    @staticmethod
    def path_to_str(path: Path):
        # bpy requires full path in str
        return str(path.absolute())


def main():
    model_path = "data/model.obj"
    output_path = "output/model.blend"
    model_path = Path(model_path)
    output_path = Path(output_path)
    scene = SimpleScene(model_path, output_path)
    print("Scene setup complete", scene)


if __name__ == "__main__":
    main()
