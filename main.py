import tyro

from model_viewer import default_dict

if __name__ == "__main__":
    tyro.extras.subcommand_cli_from_dict(default_dict)
