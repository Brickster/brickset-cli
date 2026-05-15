import json
import os
import sys
from pathlib import Path

_BRICKSET_DIRECTORY = '.brickset'
_CONFIG_FILENAME = 'config'


def _config_directory() -> Path:
    if override := os.environ.get('BRICKSET_DIR'):
        return Path(override)
    return Path.home() / _BRICKSET_DIRECTORY


def get_config() -> dict[str, str]:
    config_path = _config_directory() / _CONFIG_FILENAME
    if not config_path.exists():
        sys.exit('ERROR: no config exists. Run: brickset config API_KEY')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)


def configure(api_key: str) -> None:
    config_dir = _config_directory()
    if not config_dir.exists():
        config_dir.mkdir()
    with open(config_dir / _CONFIG_FILENAME, 'w') as config_file:
        json.dump({'api_key': api_key}, config_file)
