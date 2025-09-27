# cli.py
import os
import sys
from pathlib import Path
import yaml  # or json
from stencil.main import generate_html

def find_config():
    """Look for stencil.yaml or stencil.json in the current directory."""
    root = Path(os.getcwd())
    for file_name in ["stencil.yaml", "stencil.json"]:
        config_path = root / file_name
        if config_path.exists():
            return config_path
    return None

def main():
    config_path = find_config()
    if not config_path:
        print("Error: No stencil.yaml or stencil.json found in project root.", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        if config_path.suffix == ".yaml":
            config_data = yaml.safe_load(f)
        else:
            import json
            config_data = json.load(f)

    html_code = generate_html(config_data)

    # Output path
    # output_dir = Path("dist")
    output_dir = Path(".")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "index.html"

    with open(output_file, "w") as f:
        f.write(html_code)

    print(f"HTML generated at {output_file}")

if __name__ == "__main__":
    main()
