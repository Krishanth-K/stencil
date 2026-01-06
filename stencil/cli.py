import argparse
import json
import sys
import time
from pathlib import Path

import yaml
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from stencil.main import run
from stencil.abstract_classes.Button import Button
from stencil.abstract_classes.Input import Input
from stencil.abstract_classes.Separator import Separator
from stencil.abstract_classes.Textbox import Textbox
from stencil.abstract_classes.Title import Title

CONFIG_FILES = ["stencil.yaml", "stencil.json"]
DEFAULT_YAML_PATH = Path.cwd() / "stencil.yaml"

SUPPORTED_BACKENDS = ["html", "imgui", "curses", "flutter", "react"]


DEFAULT_YAML_CONTENT = """ # Stencil Configuration File
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

  # 'separator': A horizontal line to divide sections.
  - separator

  # 'input': A text input field.
  # 'label' is the text displayed next to the input.
  # 'placeholder' is the text that appears when the input is empty.
  - input:
      label: "Your Name"
      placeholder: "Enter your name..."

  - button:
      label: "Submit"
      callback: "doSomething"

  - text: "© 2025 Your Company"
"""


def find_config():
    root = Path.cwd()
    for f in CONFIG_FILES:
        if (root / f).exists():
            return root / f
    return None


def handle_init():
    if DEFAULT_YAML_PATH.exists():
        print(f"'{DEFAULT_YAML_PATH.name}' already exists in this directory.")
        return 0

    with open(DEFAULT_YAML_PATH, "w") as f:
        f.write(DEFAULT_YAML_CONTENT)
    print(f"Successfully created a default '{DEFAULT_YAML_PATH.name}'.")
    return 0


def generate_tree(config_data):
    tree = []
    if not isinstance(config_data, dict) or "app" not in config_data:
        raise ValueError("Invalid config: 'app' key not found.")

    for element in config_data["app"]:
        # Handle simple string elements like '- separator'
        if isinstance(element, str):
            if element == "separator":
                tree.append(Separator())
                continue
            else:
                raise ValueError(f"Invalid string element: '{element}'")

        if not isinstance(element, dict):
            raise ValueError(f"Invalid UI element format: {element}")

        element_type, value = next(iter(element.items()))

        if element_type == "title":
            tree.append(Title(value))
        elif element_type == "text":
            tree.append(Textbox(value))
        elif element_type == "button":
            if not isinstance(value, dict) or "label" not in value:
                raise ValueError(f"Invalid button format: {value}")
            tree.append(Button(text=value.pop('label'), **value))
        elif element_type == "input":
            if not isinstance(value, dict) or "label" not in value:
                raise ValueError(f"Invalid input format: {value}")
            tree.append(Input(**value))
        elif element_type == "separator":
            tree.append(Separator())
        else:
            print(f"Warning: Unknown element type '{element_type}'")
    return tree


def do_generate(args):
    config_path = find_config()
    if not config_path:
        print("Error: stencil.yaml or stencil.json not found.", file=sys.stderr)
        print("Hint: Run 'stencil init' to create a default config file.", file=sys.stderr)
        return 1

    try:
        with open(config_path) as f:
            if config_path.suffix == ".yaml":
                config_data = yaml.safe_load(f)
            else:
                config_data = json.load(f)

        tree = generate_tree(config_data)

        backend_to_use = args.backend
        if not backend_to_use:
            backend_to_use = config_data.get("config", {}).get("backend", "html")

        if backend_to_use not in SUPPORTED_BACKENDS:
            print(
                f"Error: Unsupported backend '{backend_to_use}'. Supported backends are: {', '.join(SUPPORTED_BACKENDS)}",
                file=sys.stderr,
            )
            return 1

        args.backend = backend_to_use  # Ensure args.backend is always set for run()
        run(tree, config_data, args)
    except (ValueError, TypeError) as e:
        print(f"Error processing config file '{config_path.name}': {e}", file=sys.stderr)
        return 1

    return 0


class ConfigChangeHandler(FileSystemEventHandler):
    def __init__(self, args):
        self.args = args
        # To avoid triggering multiple times for one save event
        self.last_run = 0

    def on_modified(self, event):
        if not event.is_directory and Path(event.src_path).name in CONFIG_FILES:
            # Debounce to prevent rapid firing
            if time.time() - self.last_run < 1:
                return
            print(f"\nDetected change in {Path(event.src_path).name}, regenerating...")
            # Create a shallow copy of args and set watch to False for single generation
            temp_args = argparse.Namespace(**vars(self.args))
            temp_args.watch = False
            do_generate(temp_args)
            self.last_run = time.time()


def main():
    parser = argparse.ArgumentParser(description="A tool to generate UI from a simple config file.", prog="stencil")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.2.6")
    
    # Add backend and watch arguments directly to the main parser
    parser.add_argument("-b", "--backend", type=str, default=None, help="The backend to use (html, imgui, etc.), overrides config file")
    parser.add_argument("-w", "--watch", action="store_true", help="Watch config and regenerate automatically")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser("init", help="Create a default stencil.yaml file.")

    args = parser.parse_args()

    if args.command == "init":
        return handle_init()
    else: # Default to generate
        result = do_generate(args)
        if result != 0:
            return result

        if args.watch:
            config_path = find_config()
            if not config_path:
                return 1

            event_handler = ConfigChangeHandler(args)
            observer = Observer()
            observer.schedule(event_handler, path=config_path.parent, recursive=False)
            observer.start()
            print(f"\nWatching for changes in {config_path.name}... (Press Ctrl+C to stop)")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            print("\nObserver stopped.")
            observer.join()

        return 0

if __name__ == "__main__":
    sys.exit(main())