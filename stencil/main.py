from pprint import pprint
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

        print("Using imgui backend")
        imgui_code = generate_imgui(config_data)

        with open("ui.py", "w") as f:
            f.write(imgui_code)

        print("ImGui code generated at ui.py")


#TEST: testing
config_data = {'app': [{'title': 'Admin Dashboard'},
         {'text': 'Welcome to the central control panel. Please select an '
                  'option below to proceed.'},
         {'button': {'callback': 'onViewAnalytics', 'label': 'View Analytics'}},
         {'button': {'callback': 'onManageUsers', 'label': 'Manage Users'}},
         {'button': {'callback': 'onSystemSettings',
                     'label': 'System Settings'}},
         {'text': '© 2025 Admin Corp.'}],
 'config': {'author': 'Admin Team', 'backend': 'html', 'version': '1.0.0'}}



def generate_abstract_tree(ui_data):
    
    def generate(node):

    # walk the tree
    for element in ui_data["app"]:

        if isins
