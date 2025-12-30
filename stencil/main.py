from stencil.html_backend import generate_html
from stencil.imgui_backend import generate_imgui
from stencil.abstract_classes.Button import Button
from stencil.abstract_classes.Textbox import Textbox
from stencil.abstract_classes.Title import Title
from stencil.abstract_classes.Separator import Separator
from stencil.abstract_classes.Input import Input

def run(tree, config_data, args):
    # Determine backend with correct priority: CLI > config > default
    if args.backend:
        backend = args.backend
    else:
        backend = config_data.get('config', {}).get('backend', 'html')

    if backend == "html":
        print("Using html backend")
        html_code = generate_html(tree)
        with open("index.html", "w") as f:
            f.write(html_code)
        print("HTML generated at index.html")

    elif backend == "imgui":
        print("Using imgui backend")
        imgui_code = generate_imgui(tree)
        with open("ui.py", "w") as f:
            f.write(imgui_code)
        print("ImGui code generated at ui.py")

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
            if not isinstance(value, dict) or "label" not in value or "callback" not in value:
                raise ValueError(f"Invalid button format: {value}")
            tree.append(Button(label=value["label"], callback=value["callback"]))
        elif element_type == "input":
            if not isinstance(value, dict) or "label" not in value:
                raise ValueError(f"Invalid input format: {value}")
            tree.append(Input(label=value["label"], placeholder=value.get("placeholder", "")))
        elif element_type == "separator":
            tree.append(Separator())
        else:
            print(f"Warning: Unknown element type '{element_type}'")
    return tree
