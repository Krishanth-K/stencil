import importlib
import traceback
import os

def run(tree, config_data, args):
    # Determine backend with correct priority: CLI > config > default
    backend_name = args.backend or config_data.get("config", {}).get("backend", "html")

    try:
        # Dynamically import the backend module
        backend_module = importlib.import_module(f"stencil.{backend_name}_backend")
        print(f"Using {backend_name} backend")

        # Simplified logic for each backend
        output_dir_defaults = {
            "html": "output/html",
            "react": "output/react/src", # React expects to write to a 'src' directory
            "flutter": "output/flutter_app",
            "imgui": "output/imgui",
            "curses": "output/curses",
        }
        output_dir = config_data.get("config", {}).get("output_dir", output_dir_defaults.get(backend_name, "."))

        if backend_name == "html":
            # The html backend is a function
            backend_module.generate_html(tree, output_dir)
        elif backend_name == "react":
            # The react backend is a function
            backend_module.generate_react(tree, output_dir)
        elif backend_name in ["flutter"]:
            # These backends follow a class-based approach
            BackendClass = getattr(backend_module, f"{backend_name.capitalize()}Backend")
            app = BackendClass(tree, output_dir=output_dir)
            app.generate()
        elif backend_name in ["imgui", "curses"]:
            # Legacy backends are functions
            generate_func = getattr(backend_module, f"generate_{backend_name}")
            code = generate_func(tree)
            
            os.makedirs(output_dir, exist_ok=True)
            filename = "ui.py" if backend_name == "imgui" else "tui.py"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, "w") as f:
                f.write(code)
            print(f"{backend_name.capitalize()} code generated at {filepath}")

    except ImportError:
        print(f"Error: Could not find or import the '{backend_name}' backend.")
        print("Please ensure the backend name is correct and all its dependencies are installed.")
    except Exception as e:
        print(f"An error occurred while running the {backend_name} backend: {e}")
        traceback_str = traceback.format_exc()
        print(traceback_str)