from stencil.abstract_classes.Button import Button
from stencil.abstract_classes.Textbox import Textbox
from stencil.abstract_classes.Title import Title
from stencil.abstract_classes.Separator import Separator
from stencil.abstract_classes.Input import Input


def get_head(title: str):
    css = get_css()
    return f"""
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>{title}</title>
            <style>{css}</style>
          </head>
        """

def get_title(title: str):
    return f"<h1>{title}</h1>"

def get_button(label: str, callback: str):
    return f'<button onclick="{callback}()">{label}</button>'

def get_input(label: str, placeholder: str):
    input_id = label.lower().replace(" ", "-")
    return f'<input type="text" id="{input_id}" placeholder="{placeholder}">'

def get_text(text: str):
    return f'<p>{text}</p>'

def get_stubs(callbacks: list):
    cont = "<script>\\n"
    for item in set(callbacks): # Use set to avoid duplicate functions
        stub = f"  function {item}"
        if item == "onSubmitName":
            stub += "() {\\n"
            stub += "    const name = document.getElementById('your-name').value;\\n"
            stub += "    alert('Hello, ' + (name || 'stranger') + '!');\\n"
            stub += "  }\\n"
        else:
            stub += "() {\\n"
            stub += "    // TODO: implement this\\n"
            stub += "  }\\n"
        cont += stub
    cont += "</script>"
    return cont

def get_css():
    return """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, Helvetica, sans-serif;
}
body {
    background-color: #f4f4f9;
    color: #333;
    padding: 20px;
}
h1 {
    font-size: 2rem;
    color: #2c3e50;
    margin-bottom: 20px;
    text-align: center;
}
p {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 20px;
    text-align: center;
}
button {
    background-color: #3498db;
    color: #fff;
    border: none;
    padding: 10px 20px;
    font-size: 1rem;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.2s ease;
}
button:hover {
    background-color: #2980b9;
    transform: scale(1.05);
}
.input-group {
    display: flex;
    justify-content: center;
    gap: 5px;
    margin-bottom: 20px;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
}
.input-group input {
    flex-grow: 1;
    padding: 10px;
    font-size: 1rem;
    border-radius: 5px;
    border: 1px solid #ccc;
}
.input-group button {
    flex-shrink: 0;
}
@media (max-width: 600px) {
    .input-group {
        width: 95%;
    }
    button {
        width: auto; /* Revert button width for non-standalone buttons */
    }
}
"""

def generate_html(tree):
    if not tree:
        raise ValueError("The UI tree is empty. Nothing to generate.")

    head = ""
    body = ""
    callbacks = []

    title_node = next((node for node in tree if isinstance(node, Title)), None)
    if title_node:
        head = get_head(title_node.text)
        body += get_title(title_node.text)
    else:
        head = get_head("Stencil Generated Page")
        print("Warning: No title found in config. Using a default title.")

    i = 0
    while i < len(tree):
        node = tree[i]
        
        if isinstance(node, Input) and (i + 1) < len(tree) and isinstance(tree[i+1], Button):
            input_node = node
            button_node = tree[i+1]
            input_html = get_input(input_node.label, input_node.placeholder)
            button_html = get_button(button_node.label, button_node.callback)
            body += f'<div class="input-group">{input_html}{button_html}</div>'
            callbacks.append(button_node.callback)
            i += 2
            continue

        if isinstance(node, Textbox):
            body += get_text(node.text)
        elif isinstance(node, Button):
            body += get_button(node.label, node.callback)
            callbacks.append(node.callback)
        elif isinstance(node, Separator):
            body += "<hr />"
        elif isinstance(node, Input):
            body += get_input(node.label, node.placeholder)
        elif isinstance(node, Title):
            pass
        else:
            print(f"Warning: HTML backend does not support node type: {type(node)}")
        
        i += 1

    close_body = """
                </body>
                </html>
            """
    stubs = get_stubs(callbacks)
    content = head + "<body>" + body + stubs + close_body
    return content
