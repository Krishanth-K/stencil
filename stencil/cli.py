import argparse
from pathlib import Path
import yaml
import json
import sys
from stencil.main import run

CONFIG_FILES = ["stencil.yaml", "stencil.json"]

def find_config():
    root = Path.cwd()
    for f in CONFIG_FILES:
        if (root / f).exists():
            return root / f
    return None

def main():
    parser = argparse.ArgumentParser(description="Generate files from stencil.yaml/json")
    parser.add_argument("-w", "--watch", action="store_true", help="Watch config and regenerate automatically")
    parser.add_argument("-b", "--backend", type=str, default="html", help="The backend to use (html, imgui)")
    args = parser.parse_args()

    config_path = find_config()
    if not config_path:
        print("Error: stencil.yaml or stencil.json not found.", file=sys.stderr)
        return 1

    with open(config_path) as f:
        if config_path.suffix == ".yaml":
            config_data = yaml.safe_load(f)
        else:
            config_data = json.load(f)

    run(config_data, args)

