from pprint import pprint
import yaml


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
        stub += "{\
                    // TODO: implement this\
                }\
                "
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


def generate_html(data):
    data_list = data.get("app")  # renamed to avoid shadowing 'data'
    if not data_list:
        raise ValueError("Config must have a top-level 'app' key with a list of elements")


    head = ""
    body = ""
    callbacks = []

    for element in data_list:
        for attr, value in element.items():
            if attr == "title":
                head = get_head(value)

            if attr == "button":
                but : str = get_button(value["label"], value["callback"])
                body += but

                callbacks.append(value["callback"])


            if attr == "text":
                text : str = get_text(value)
                body += text

    close_header = """
                </body>
                </html>
            """

    if head == "":
        print("Error: no title")

    stubs = get_stubs(callbacks)
    content = head + "<body>" + body + close_header + stubs

    return content

#
# with open("stencil.yaml", 'r') as f:
#     data = yaml.safe_load(f)
#     pprint(data)
#
#     content = generate_html(data)
#     write_to_file(content)
#
