from stencil.html_backend import generate_html
from stencil.imgui_backend import generate_imgui

def run(config_data, args):
    backend = args.backend
    if backend == 'html' and 'backend' in config_data:
        backend = config_data['backend']

    if backend == "html":
        print("Using html backend")
        html_code = generate_html(config_data)
        with open("index.html", "w") as f:
            f.write(html_code)
        print("HTML generated at index.html")
    elif backend == "imgui":
        imgui_code = generate_imgui(config_data)
        with open("ui.py", "w") as f:
            f.write(imgui_code)
        print("ImGui code generated at ui.py")
