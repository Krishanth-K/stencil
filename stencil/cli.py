import argparse
import json
import sys
import time
from pathlib import Path

import yaml
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from stencil.abstract_classes.Button import Button
from stencil.abstract_classes.Input import Input
from stencil.abstract_classes.Separator import Separator
from stencil.abstract_classes.Text import Text
from stencil.main import run

# Initialize Rich Console
console = Console()

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
config:
  backend: "html"
  version: "1.0.0"
  author: "Your Name"

app:
  - title: "My Awesome App"
  - text: |
      Welcome to Stencil!
      This is a simple example of a UI defined in YAML.
  - button:
      label: "Click Me!"
      callback: "onButtonClick"
  - separator
  - input:
      label: "Your Name"
      placeholder: "Enter your name..."
  - button:
      label: "Submit"
      callback: "doSomething"
  - text: "© 2025 Your Company"
"""


def find_config() -> Path | None:
    current = Path.cwd()
    while True:
        for filename in CONFIG_FILES:
            path = current / filename
            if path.exists():
                return path
        parent = current.parent
        if parent == current:
            return None
        current = parent


def load_config(config_path):
    try:
        with open(config_path) as f:
            if config_path.suffix == ".yaml":
                config_data = yaml.safe_load(f)
            else:
                config_data = json.load(f)
        return config_data
    except Exception as e:
        console.print(f"[bold red]Error loading config:[/bold red] {e}")
        return None


def handle_init() -> int:
    if DEFAULT_YAML_PATH.exists():
        console.print(f"[yellow]'{DEFAULT_YAML_PATH.name}' already exists in this directory.[/yellow]")
        return 0
    with open(DEFAULT_YAML_PATH, "w") as f:
        f.write(DEFAULT_YAML_CONTENT)
    console.print(Panel(f"[bold green]Successfully created a default '{DEFAULT_YAML_PATH.name}'.[/bold green]"))
    return 0


def handle_list() -> int:
    """List all available backends and their supported elements."""
    backends_dir = Path(__file__).parent / "backends"
    if not backends_dir.exists():
        console.print("[bold red]Error:[/bold red] Backends directory not found.")
        return 1

    table = Table(title="[bold blue]Available Stencil Backends[/bold blue]")
    table.add_column("Backend", style="cyan", no_wrap=True)
    table.add_column("Version", style="magenta")
    table.add_column("Supported Elements", style="green")

    for backend_path in sorted(backends_dir.iterdir()):
        if backend_path.is_dir():
            manifest_path = backend_path / "backend.yaml"
            if manifest_path.exists():
                with open(manifest_path) as f:
                    manifest = yaml.safe_load(f)
                    name = manifest.get("name", backend_path.name)
                    version = manifest.get("version", "N/A")
                    elements = ", ".join(manifest.get("supported_elements", []))
                    table.add_row(name, version, elements)

    console.print(table)
    return 0


def generate_tree(config_data: dict) -> list:
    tree = []
    if "app" not in config_data:
        raise ValueError("Config missing 'app' section.")

    for element in config_data["app"]:
        if isinstance(element, str):
            element = {element: None}
        element_type, value = next(iter(element.items()))
        cls = COMPONENT_MAP.get(element_type)
        if cls is None:
            console.print(f"[bold yellow]Warning:[/bold yellow] Unknown element type '{element_type}'")
            continue

        try:
            if value is None:
                tree.append(cls())
            elif isinstance(value, dict):
                tree.append(cls(**value))
            else:
                tree.append(cls(value))
        except Exception as e:
            console.print(f"[bold red]Error parsing element '{element_type}':[/bold red] {e}")
            raise

    return tree


def resolve_backend(args: argparse.Namespace, config_data: dict) -> str | None:
    backend = args.backend or config_data.get("config", {}).get("backend", "html")
    backends_dir = Path(__file__).parent / "backends"

    if not (backends_dir / backend).exists():
        console.print(f"[bold red]Error:[/bold red] Backend '{backend}' not found in backends directory.", style="red")
        return None

    return backend


def build(args: argparse.Namespace) -> int:
    config_path = find_config()
    if not config_path:
        console.print("[bold red]Error:[/bold red] stencil.yaml or stencil.json not found.")
        console.print("[blue]Hint:[/blue] Run [bold]stencil init[/bold] to create a default config file.")
        return 1

    try:
        config_data = load_config(config_path)
        if config_data is None:
            return 1

        tree = generate_tree(config_data)
        backend = resolve_backend(args, config_data)
        if backend is None:
            return 1

        with console.status(f"[bold green]Generating {backend} backend..."):
            run(tree, config_data, args)

        console.print(f"[bold green]✔  Done![/bold green] Generated output using [bold]{backend}[/bold] backend.")

    except Exception as e:
        console.print(f"[bold red]Error during build:[/bold red] {e}")
        return 1

    return 0


class ConfigChangeHandler(FileSystemEventHandler):
    def __init__(self, args):
        self.args = args
        self.last_run = 0

    def on_modified(self, event):
        if not event.is_directory and Path(event.src_path).name in CONFIG_FILES:
            if time.time() - self.last_run < 1:
                return
            console.print(f"\n[bold blue]Detected change in {Path(event.src_path).name}, regenerating...[/bold blue]")
            temp_args = argparse.Namespace(**vars(self.args))
            temp_args.watch = False
            build(temp_args)
            self.last_run = time.time()


def _watch(args: argparse.Namespace) -> None:
    config_path = find_config()
    if not config_path:
        return

    observer = Observer()
    observer.schedule(ConfigChangeHandler(args), path=str(config_path.parent), recursive=False)
    observer.start()
    console.print(f"\n[bold cyan]Watching {config_path.name} for changes...[/bold cyan] (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()
        console.print("\n[bold yellow]Stopped watching.[/bold yellow]")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate UI from a simple config file.", prog="stencil")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0.0")
    parser.add_argument("-b", "--backend", type=str, default=None, help="Backend to use. Overrides config file.")
    parser.add_argument("-w", "--watch", action="store_true", help="Watch config file and regenerate on change.")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("init", help="Create a default stencil.yaml in the current directory.")
    subparsers.add_parser("list", help="List available backends and their supported elements.")

    args = parser.parse_args()

    if args.command == "init":
        return handle_init()
    elif args.command == "list":
        return handle_list()
    else:
        result = build(args)
        if result == 0 and args.watch:
            _watch(args)
        return result


if __name__ == "__main__":
    sys.exit(main())
