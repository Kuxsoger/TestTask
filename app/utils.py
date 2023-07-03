from pathlib import Path

import yaml


root_dir = Path(__file__).absolute().resolve().parent.parent


def load_yaml_file(filename: Path) -> dict:
    with open(root_dir / filename) as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)
