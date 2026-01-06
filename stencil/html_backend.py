import os
from pathlib import Path

# Assuming this script is in stencil/
STYLE_PATH = Path(__file__).parent / "style.css"

def generate_html(tree, output_dir="output/html"):
    """
    Generates an index.html file and a style.css file from the UI tree.
    """
    if not tree:
        raise ValueError("The UI tree is empty. Nothing to generate.")

    # 1. Ensure output directory exists and write style.css
    os.makedirs(output_dir, exist_ok=True)
    try:
        with open(STYLE_PATH, "r") as f:
            css_content = f.read()
        with open(os.path.join(output_dir, "style.css"), "w") as f:
            f.write(css_content)
    except FileNotFoundError:
        print("Warning: stencil/style.css not found. No styles will be applied.")
        css_content = "/* CSS file not found */"


    # 2. Generate HTML content
    title = "Stencil App"
    title_node = next((node for node in tree if node.__class__.__name__ == 'Title'), None)
    if title_node:
        title = title_node.text

    body_elements = []
    callbacks = set()

    for component in tree:
        comp_type = component.__class__.__name__
        if comp_type == "Title":
            body_elements.append(f"<h1>{component.text}</h1>")
        elif comp_type == "Textbox":
            # Check for footer text
            if "©" in component.text:
                 body_elements.append(f'<p class="footer">{component.text}</p>')
            else:
                body_elements.append(f"<p>{component.text}</p>")
        elif comp_type == "Button":
            body_elements.append(f'<button onclick="{getattr(component, "callback", "")}">{component.text}</button>')
            if hasattr(component, "callback"):
                callbacks.add(component.callback)
        elif comp_type == "Input":
            label = getattr(component, 'label', '')
            name = getattr(component, 'name', label.lower().replace(' ', '_'))
            placeholder = getattr(component, 'placeholder', '')
            body_elements.append(f'''
<div class="input-group">
    <label for="{name}">{label}</label>
    <input type="text" id="{name}" name="{name}" placeholder="{placeholder}">
</div>
''')
        elif comp_type == "Separator":
            body_elements.append('<hr class="separator">')

    # 3. Generate JavaScript stubs for callbacks
    js_stubs = []
    for cb in callbacks:
        js_stubs.append(f"function {cb}() {{ console.log('{cb} called'); alert('{cb} not implemented'); }}")
    
    script_content = "\\n".join(js_stubs)

    # 4. Assemble the final HTML file
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        {''.join(body_elements)}
    </div>
    <script>
        {script_content}
    </script>
</body>
</html>
"""

    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(html_content)
    
    print(f"HTML and CSS files generated in '{output_dir}' directory.")

# Note: The old functions get_head, get_css etc. are now obsolete and removed.
# The main generation logic is consolidated into the single generate_html function.
