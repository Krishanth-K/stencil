import argparse
import json
import sys
from pathlib import Path

import yaml

from stencil.main import generate_tree, run

CONFIG_FILES = ["stencil.yaml", "stencil.json"]
DEFAULT_YAML_PATH = Path.cwd() / "stencil.yaml"

DEFAULT_YAML_CONTENT = """# Stencil Configuration File
# --------------------------
# This file is used to define the UI elements for your application.
# You can generate different outputs (like HTML or a desktop app) from the same config.

# Optional configuration for the project
config:
  # The backend determines the output format.
  # Supported backends: "html", "imgui"
  # Default is "html".
  backend: "html"
  version: "1.0.0"
  author: "Your Name"

# The 'app' section defines the sequence of UI elements to be rendered.
app:
  # 'title': Sets the main title of the page or window.
  - title: "My Awesome App"

  # 'text': A block of text. Can be multi-line using the '|' character.
  - text: |
      Welcome to Stencil!
      This is a simple example of a UI defined in YAML.

  # 'button': A clickable button.
  # 'label' is the text on the button.
  # 'callback' is the function name that will be called when clicked.
  # Stencil generates a placeholder for this function.
  - button:
      label: "Click Me!"
      callback: "onButtonClick"

  - separator

  # 'input': A text input field.
  # 'label' is the visible label for the field.
  # 'placeholder' is the text shown when the field is empty.
  - input:
      label: "Your Name"
      placeholder: "Enter your name here"
  - button:
      label: "Submit"
      callback: "onSubmitName"

  - text: "© 2025 Your Company"
"""


def find_config():
    root = Path.cwd()
    for f in CONFIG_FILES:
        if (root / f).exists():
            return root / f
    return None


def handle_init():
    """Creates a default stencil.yaml file in the current directory."""
    if DEFAULT_YAML_PATH.exists():
        print(f"'{DEFAULT_YAML_PATH.name}' already exists in this directory.")
        return 0

    with open(DEFAULT_YAML_PATH, "w") as f:
        f.write(DEFAULT_YAML_CONTENT)
    print(f"Successfully created a default '{DEFAULT_YAML_PATH.name}'.")
    return 0


def do_generate(args):
    """Finds config, generates tree, and runs the backend."""
    config_path = find_config()
    if not config_path:
        print("Error: stencil.yaml or stencil.json not found.", file=sys.stderr)
        print("Hint: Run 'stencil init' to create a default config file.", file=sys.stderr)
        return 1

    with open(config_path) as f:
        if config_path.suffix == ".yaml":
            config_data = yaml.safe_load(f)
        else:
            config_data = json.load(f)

    try:
        tree = generate_tree(config_data)
        run(tree, config_data, args)
    except (ValueError, TypeError) as e:
        print(f"Error processing config file '{config_path.name}': {e}", file=sys.stderr)
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(description="A tool to generate UI from a simple config file.", prog="stencil")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Init Command ---
    init_parser = subparsers.add_parser("init", help="Create a default stencil.yaml file.")

    # --- Generate Command (default) ---
    gen_parser = subparsers.add_parser("generate", help="Generate UI from config file (default action).")
    gen_parser.add_argument("-w", "--watch", action="store_true", help="Watch config and regenerate automatically")
    gen_parser.add_argument(
        "-b", "--backend", type=str, default=None, help="The backend to use (html, imgui), overrides config file"
    )

    # If no command is given, default to 'generate'
    args = parser.parse_args(sys.argv[1:] if sys.argv[1:] else ["generate"])

    if args.command == "init":
        return handle_init()
    elif args.command == "generate":
        return do_generate(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
