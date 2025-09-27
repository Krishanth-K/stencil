import argparse
from pathlib import Path
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from stencil.main import generate_html
import yaml
import json

CONFIG_FILES = ["stencil.yaml", "stencil.json"]

def find_config():
    root = Path.cwd()
    for f in CONFIG_FILES:
        if (root / f).exists():
            return root / f
    return None

def build_html(config_path):
    with open(config_path) as f:
        if config_path.suffix == ".yaml":
            config_data = yaml.safe_load(f)
        else:
            config_data = json.load(f)
    html_code = generate_html(config_data)
    output_file = Path(".") / "index.html"
    with open(output_file, "w") as f:
        f.write(html_code)
    print(f"HTML generated at {output_file}")

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, config_path):
        self.config_path = config_path

    def on_modified(self, event):
        if Path(event.src_path).resolve() == self.config_path.resolve():
            print(f"{self.config_path} changed, regenerating HTML...")
            build_html(self.config_path)
            print("Done!\n")

def main():
    parser = argparse.ArgumentParser(description="Generate HTML from stencil.yaml/json")
    parser.add_argument("--watch", action="store_true", help="Watch config and regenerate automatically")
    args = parser.parse_args()

    config_path = find_config()
    if not config_path:
        print("Error: stencil.yaml or stencil.json not found.", file=sys.stderr)
        return 1

    build_html(config_path)

    if args.watch:
        event_handler = ReloadHandler(config_path)
        observer = Observer()
        observer.schedule(event_handler, path=".", recursive=False)
        observer.start()
        print("Watching config for changes. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

