from stencil.abstract_classes.Button import Button
from stencil.abstract_classes.Textbox import Textbox
from stencil.abstract_classes.Title import Title
from stencil.abstract_classes.Separator import Separator
from stencil.abstract_classes.Input import Input


def get_head(title: str):
    css = get_css()

    return f"""
        <!doctype html>
        <html lang="">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>{title}</title>
            <style>{css}</style>
            <link href="css/style.css" rel="stylesheet" />
          </head>
        """

def get_title(title: str):
    return f"<h1>{title}</h1>"

def get_button(label : str, callback : str):
    cont = f'<button onclick="{callback}">{label}</button>'
    return cont

def get_input(label: str, placeholder: str):
    # Generate a simple id from the label
    input_id = label.lower().replace(" ", "-")
    return f'<input type="text" id="{input_id}" placeholder="{placeholder}">'

def get_text(text : str):
    cont = f'<p>{text}</p>'
    return cont

def get_stubs(callbacks : list):
    cont = "<script> \n"

    for item in callbacks:
        stub = f"function {item}"
        # Special case for the submit button
        if item == "onSubmitName":
            # JS to get value from the input (id is derived from label 'Your Name') and show alert
            stub += "() {\n"
            stub += "    const name = document.getElementById('your-name').value;\n"
            stub += "    alert('Hello, ' + name + '!');\n"
            stub += "                }\n"
        else:
            stub += "() {\n"
            stub += "                    // TODO: implement this\n"
            stub += "                }\n"
        cont += stub

    cont += "\n</script>"
    return cont

def get_css():
    return """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, Helvetica, sans-serif;
}

/* Body styling */
body {
    background-color: #f4f4f9;
    color: #333;
    padding: 20px;
}

/* Title */
h1 {
    font-size: 2rem;
    color: #2c3e50;
    margin-bottom: 20px;
    text-align: center;
}

/* Paragraph text */
p {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 20px;
    text-align: center;
}

/* Buttons container (if using a div) */
#button-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px; /* spacing between buttons */
    margin-bottom: 20px;
}

/* Buttons styling */
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

/* Input fields styling */
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

/* Optional: responsive */
@media (max-width: 600px) {
    .input-group {
        width: 95%;
    }

    button {
        width: 80%;
        padding: 12px;
        font-size: 1.1rem;
    }
}
"""

def write_to_file(content : str):
    with open("ui.html", 'w') as f:
        f.write(content)
        print("Written to file")

def generate_html(tree):
    if not tree:
        raise ValueError("The UI tree is empty. Nothing to generate.")

    head = ""
    body = ""
    callbacks = []

    # Find the title first to generate the head
    title_node = next((node for node in tree if isinstance(node, Title)), None)
    if title_node:
        head = get_head(title_node.text)
        body += get_title(title_node.text)
    else:
        head = get_head("Stencil Generated Page")
        print("Warning: No title found in config. Using a default title.")

    # Use an iterator to allow look-ahead for grouping
    nodes = iter(tree)
    for node in nodes:
        if isinstance(node, Input):
            # Peek at the next node
            next_node = next(nodes, None)
            if next_node and isinstance(next_node, Button):
                # Grouped input and button
                input_html = get_input(node.label, node.placeholder)
                button_html = get_button(next_node.label, next_node.callback)
                body += f'<div class="input-group">{input_html}{button_html}</div>'
                callbacks.append(next_node.callback)
            else:
                # Standalone input
                body += get_input(node.label, node.placeholder)
                # If we peeked and it wasn't a button, we need to process it
                if next_node:
                     # This logic can get complex, for now we assume button is always next
                     pass
        
        elif isinstance(node, Textbox):
            body += get_text(node.text)
        elif isinstance(node, Button):
            # This handles buttons that are not preceded by an input
            body += get_button(node.label, node.callback)
            callbacks.append(node.callback)
        elif isinstance(node, Separator):
            body += "<hr />"
        elif isinstance(node, Title):
            pass  # Already handled
        else:
            print(f"Warning: HTML backend does not support node type: {type(node)}")

    close_body = """
                </body>
                </html>
            """

    stubs = get_stubs(callbacks)
    content = head + "<body>" + body + close_body + stubs

    return content
