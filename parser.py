from pprint import pprint
import yaml


def get_title(title: str):
    return f"""
        <!doctype html>
        <html lang="">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>{title}</title>
            <link href="css/style.css" rel="stylesheet" />
          </head>
          <body>
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



def write_to_file(content : str):
    with open("ui.html", 'w') as f:
        f.write(content)
        print("Written to file")




with open("sten.yaml", 'r') as f:
    data = yaml.safe_load(f)




data : list[dict] = data.get("app")

title = ""
body = ""
callbacks = []

for element in data:
    for attr, value in element.items():
        if attr == "title":
            body += get_title(value)

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

if title == "":
    print("Error: no title")


stubs = get_stubs(callbacks)

content = title + body + close_header + stubs


write_to_file(content)

pprint(content)
