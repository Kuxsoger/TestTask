from pathlib import Path

import yaml


test_data_dir = Path(__file__).absolute().resolve().parent / "test_data"


def load_yaml_file(filename: Path) -> dict:
    with open(test_data_dir / filename) as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)
