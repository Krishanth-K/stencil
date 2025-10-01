from html_backend import generate_html
from imgui_backend import generate_imgui
from yaml import safe_load
from pprint import pprint

def generate_ui(data):
    backend = data.get("backend")

    if not backend or backend == "html":
        return generate_html(data)
    elif backend == "imgui":
        return generate_imgui(data)


with open("stencil.yaml", 'r') as f:
    content = f.read()
    content = safe_load(content)

    # print(content)
    pprint(generate_ui(content))
