import os
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

BACKENDS_DIR = Path(__file__).parent / "backends"


def render_app(tree: list, backend_name: str, output_dir: str = None, config_data: dict = None) -> None:
    """
    The unified engine. Renders a tree of components using Jinja2 templates
    from the specified backend folder and writes the output to disk.
    """
    backend_path = BACKENDS_DIR / backend_name
    manifest_path = backend_path / "backend.yaml"

    if not backend_path.exists() or not manifest_path.exists():
        raise ValueError(f"Backend '{backend_name}' not found in {BACKENDS_DIR}")

    # 1. Load manifest
    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    output_dir = config_data.get("config", {}).get("output_dir") if config_data else None
    output_dir = output_dir or manifest.get("default_output_dir", "output")
    output_filename = manifest.get("output_filename", "output.txt")

    # 2. Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(backend_path)))

    # 3. Render each component
    body_elements = []
    callbacks = set()
    input_fields = []
    interactive_indices = []

    for i, component in enumerate(tree):
        comp_type = component.__class__.__name__

        # Build context from object attributes
        context = {k: v for k, v in vars(component).items() if not k.startswith("_")}

        # Collect layout ingredients
        if getattr(component, "callback", None):
            callbacks.add(component.callback)
        if getattr(component, "is_interactive", False):
            interactive_indices.append(i)
        if comp_type == "Input":
            input_fields.append(context)

        # Render component template
        try:
            template = env.get_template(f"{comp_type}.j2")
            body_elements.append(template.render(**context))
        except TemplateNotFound:
            print(f"Warning: No template for '{comp_type}' in '{backend_name}' backend, skipping.")

    # 4. Build layout context
    app_name = (config_data or {}).get("config", {}).get("name") or os.path.basename(os.getcwd())
    title = next(
        (getattr(c, "text", getattr(c, "content", None)) for c in tree if c.__class__.__name__ in ["Title", "Text"]),
        app_name,
    )

    layout_context = {
        "body_elements": body_elements,
        "title": title,
        "app_name": app_name,
        "callbacks": sorted(callbacks),
        "input_fields": input_fields,
        "interactive_widgets": interactive_indices,
        "config": config_data or {},
    }

    # 5. Render layout
    final_output = env.get_template("_layout.j2").render(**layout_context)

    # 6. Write output
    target_file = Path(output_dir) / output_filename
    target_file.parent.mkdir(parents=True, exist_ok=True)
    with open(target_file, "w") as f:
        f.write(final_output)

    # 7. Copy extra files
    for filename in manifest.get("copy_files", []):
        src = backend_path / filename
        if src.exists():
            shutil.copy(src, Path(output_dir) / filename)

    print(f"Generated '{backend_name}' backend at: {target_file}")
