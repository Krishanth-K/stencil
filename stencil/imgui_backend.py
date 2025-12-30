import sys
import re
from stencil.abstract_classes.Button import Button
from stencil.abstract_classes.Textbox import Textbox
from stencil.abstract_classes.Title import Title
from stencil.abstract_classes.Separator import Separator
from stencil.abstract_classes.Input import Input

def _sanitize_label_for_variable(label):
    """Turns a string label into a valid Python variable name."""
    s = re.sub(r'\W|^(?=\d)', '_', label)
    return f"input_buffer_{s.lower()}"

def generate_imgui(tree):
    """
    Generates a standalone Python file (ui.py) that renders an ImGui interface
    based on the provided UI tree.
    """
    if not tree:
        raise ValueError("The UI tree is empty. Nothing to generate.")

    title_node = next((node for node in tree if isinstance(node, Title)), None)
    title = title_node.text if title_node else "ImGui Window"

    callback_defs = ""
    buffer_defs = ""
    render_logic = ""
    global_statements = ""


    # First pass: Create callback and buffer definitions
    for node in tree:
        if isinstance(node, Button):
            cb_name = node.callback
            # Special case for the submit button to create an interactive callback
            if cb_name == "onSubmitName":
                var_name = _sanitize_label_for_variable("Your Name") # Assumes input with label "Your Name"
                callback_defs += f'''
def {cb_name}():
    print(f"Value submitted from '{var_name}': {{{var_name}}}")
'''
            else:
                callback_defs += f'''
def {cb_name}():
    print("Callback '{cb_name}' triggered")
'''
        elif isinstance(node, Input):
            var_name = _sanitize_label_for_variable(node.label)
            # Initialize buffer with placeholder text
            buffer_defs += f'{var_name} = "{node.placeholder}"\n'
            global_statements += f'    global {var_name}\n'

    # Second pass: Build the rendering logic
    for node in tree:
        if isinstance(node, Textbox):
            render_logic += f'        imgui.text("""{node.text}""")\n'
        elif isinstance(node, Button):
            render_logic += f'        if imgui.button("{node.label}"):\n            {node.callback}()\n'
        elif isinstance(node, Separator):
            render_logic += '        imgui.separator()\n'
        elif isinstance(node, Input):
            var_name = _sanitize_label_for_variable(node.label)
            # In ImGui, the placeholder is shown if the buffer is empty.
            render_logic += f'        changed, {var_name} = imgui.input_text("{node.label}", {var_name}, 256)\n'
        elif isinstance(node, Title):
            render_logic += f'        imgui.text_ansi("{node.text}")\n'
        else:
            print(f"Warning: ImGui backend does not support node type: {type(node)}")

    # Assemble the full code for ui.py
    content = f'''import sys
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer

# Define buffers for input fields
{buffer_defs}

{callback_defs}

def main():
{global_statements}
    if not glfw.init():
        print("Could not initialize GLFW")
        sys.exit(1)

    window = glfw.create_window(1280, 720, "{title}", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)
    imgui.create_context()
    renderer = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        renderer.process_inputs()
        imgui.new_frame()

        imgui.begin("{title}")
{render_logic}
        imgui.end()

        gl.glClearColor(0.1, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        renderer.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    renderer.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
'''
    return content
