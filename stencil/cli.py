import argparse
import json
import sys
import time
from pathlib import Path
from pprint import pprint

import yaml
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from stencil.abstract_classes.Button import Button
from stencil.abstract_classes.Input import Input
from stencil.abstract_classes.Separator import Separator
from stencil.abstract_classes.Text import Text
from stencil.main import run

from .engine import render_app

CONFIG_FILES = ["stencil.yaml", "stencil.json"]
DEFAULT_YAML_PATH = Path.cwd() / "stencil.yaml"

SUPPORTED_BACKENDS = ["html", "imgui", "curses", "flutter", "react"]

COMPONENT_MAP = {
    "title": Text,
    "text": Text,
    "button": Button,
    "input": Input,
    "separator": Separator,
}


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


def find_config() -> Path | None:
    """
    Search for stencil.yaml, starting from current directory and walking up until reaching filesystem root.
    """
    current = Path.cwd()
    while True:
        for filename in CONFIG_FILES:
            path = current / filename
            if path.exists():
                return path
        parent = current.parent
        if parent == current:  # reached filesystem root
            return None
        current = parent


def load_config(config_path):
    """Load data from a config file, with the path to the file."""
    with open(config_path) as f:
        if config_path.suffix == ".yaml":
            config_data = yaml.safe_load(f)
        else:
            config_data = json.load(f)

    return config_data


def handle_init() -> int:
    """
    Create a default stencil.yaml in the current directory.
    Does nothing if the file already exists.
    Returns 0 on success.
    """
    if DEFAULT_YAML_PATH.exists():
        print(f"'{DEFAULT_YAML_PATH.name}' already exists in this directory.")
        return 0
    with open(DEFAULT_YAML_PATH, "w") as f:
        f.write(DEFAULT_YAML_CONTENT)
    print(f"Successfully created a default '{DEFAULT_YAML_PATH.name}'.")
    return 0


def generate_tree(config_data: dict) -> list:
    """
    Build a list of Component objects from the parsed config data.
    Each element in config_data['app'] maps to a component class via COMPONENT_MAP.
    Unknown element types are skipped with a warning.
    """
    tree = []
    for element in config_data["app"]:
        if isinstance(element, str):
            element = {element: None}  # handle bare elements like "separator"
        element_type, value = next(iter(element.items()))
        cls = COMPONENT_MAP.get(element_type)
        if cls is None:
            print(f"Warning: Unknown element type '{element_type}'")
            continue
        if value is None:
            tree.append(cls())
        elif isinstance(value, dict):
            tree.append(cls(**value))
        else:
            tree.append(cls(value))  # bare string value like title or text
    return tree


def resolve_backend(args: argparse.Namespace, config_data: dict) -> str | None:
    """
    Resolve the backend to use, with priority: CLI flag > config file > default (html).
    Returns None if the resolved backend is not supported.
    """
    backend = args.backend or config_data.get("config", {}).get("backend", "html")
    if backend not in SUPPORTED_BACKENDS:
        print(f"Error: Unsupported backend '{backend}'. Supported: {', '.join(SUPPORTED_BACKENDS)}", file=sys.stderr)
        return None
    return backend


def build(args: argparse.Namespace) -> int:
    """
    Main build pipeline: find config, load it, build the component tree, and run the engine.
    Returns 0 on success, 1 on failure.
    """

    config_path = find_config()
    if not config_path:
        print("Error: stencil.yaml or stencil.json not found.", file=sys.stderr)
        print("Hint: Run 'stencil init' to create a default config file.", file=sys.stderr)
        return 1

    try:
        # load config
        config_data = load_config(config_path)
        if config_data is None:
            print("Error: Config file is empty.", file=sys.stderr)
            return 1

        # build component tree
        tree = generate_tree(config_data)

        # resolve the backend to use
        backend = resolve_backend(args, config_data)
        if backend is None:
            return 1

        # run(tree, config_data, backend)
        render_app(tree, backend, config_data=config_data)

    except (ValueError, TypeError) as e:
        print(f"Error processing '{config_path.name}': {e}", file=sys.stderr)
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
            build(temp_args)
            self.last_run = time.time()


def _run_generate(args: argparse.Namespace) -> int:
    result = build(args)
    if result != 0:
        return result

    if args.watch:
        _watch(args)

    return 0


def _watch(args: argparse.Namespace) -> None:
    config_path = find_config()
    if not config_path:
        print("Error: No config file found to watch.", file=sys.stderr)
        return

    observer = Observer()
    observer.schedule(ConfigChangeHandler(args), path=str(config_path.parent), recursive=False)
    observer.start()
    print(f"\nWatching {config_path.name} for changes... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()
        print("\nStopped watching.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate UI from a simple config file.", prog="stencil")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.2.6")
    parser.add_argument(
        "-b", "--backend", type=str, default=None, help="Backend to use (html, imgui, curses). Overrides config file."
    )
    parser.add_argument("-w", "--watch", action="store_true", help="Watch config file and regenerate on change.")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("init", help="Create a default stencil.yaml in the current directory.")

    args = parser.parse_args()

    match args.command:
        case "init":
            return handle_init()
        case _:
            return _run_generate(args)
            # test()
            return 0


def test():
    config_path = find_config()
    if not config_path:
        print("Error: stencil.yaml or stencil.json not found.", file=sys.stderr)
        print("Hint: Run 'stencil init' to create a default config file.", file=sys.stderr)
        return 1

    # load config
    config_data = load_config(config_path)
    if config_data is None:
        print("Error: Config file is empty.", file=sys.stderr)
        return 1

    pprint(config_data)


if __name__ == "__main__":
    sys.exit(main())
