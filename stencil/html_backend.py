from stencil.abstract_classes.Button import Button
from stencil.abstract_classes.Textbox import Textbox
from stencil.abstract_classes.Title import Title


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

def get_text(text : str):
    cont = f'<p>{text}</p>'
    return cont

def get_stubs(callbacks : list):
    cont = "<script> \n"

    for item in callbacks:
        stub = f"function {item}"
        stub += "() {\
                    // TODO: implement this\
                }\
                "
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

/* Optional: responsive */
@media (max-width: 600px) {
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
        # Default title if none is provided in the config
        head = get_head("Stencil Generated Page")
        print("Warning: No title found in config. Using a default title.")


    for node in tree:
        if isinstance(node, Textbox):
            body += get_text(node.text)
        elif isinstance(node, Button):
            body += get_button(node.label, node.callback)
            callbacks.append(node.callback)
        elif isinstance(node, Title):
            pass # Already handled
        else:
            print(f"Warning: HTML backend does not support node type: {type(node)}")


    close_body = """
                </body>
                </html>
            """

    stubs = get_stubs(callbacks)
    content = head + "<body>" + body + close_body + stubs

    return content
