from pprint import pprint
import yaml

with open("sten.yaml", 'r') as f:
    data = yaml.safe_load(f)

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

def write_to_file(content : str):
    with open("ui.html", 'w') as f:
        f.write(content)
        print("Written to file")


data : list[dict] = data.get("app")
pprint(data)


title = ""
body = ""

for element in data:
    for attr, value in element.items():
        if attr == "title":
            body += get_title(value)

        if attr == "button":
            but : str = get_button(value["label"], value["callback"])
            body += but

        if attr == "text":
            text : str = get_text(value)
            body += text

close_header = """
            </body>
            </html>
        """

if title == "":
    print("Error: no title")

content = title + body + close_header


write_to_file(content)

pprint(content)
