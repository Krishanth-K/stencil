import sys
from stencil.abstract_classes.Button import Button
from stencil.abstract_classes.Textbox import Textbox
from stencil.abstract_classes.Title import Title

def generate_imgui(tree):
    """
    Generates a standalone Python file (ui.py) that renders an ImGui interface
    based on the provided UI tree.
    """
    if not tree:
        raise ValueError("The UI tree is empty. Nothing to generate.")

    # Find the title first to use as the window title
    title_node = next((node for node in tree if isinstance(node, Title)), None)
    title = title_node.text if title_node else "ImGui Window"

    # --- Create callback stubs ---
    callback_defs = ""
    for node in tree:
        if isinstance(node, Button):
            cb_name = node.callback
            callback_defs += f"""
def {cb_name}():
    print("Callback '{cb_name}' triggered")
"""

    # --- Build the ImGui rendering logic ---
    render_logic = ""
    for node in tree:
        if isinstance(node, Textbox):
            # Use triple quotes for multi-line text
            render_logic += f'        imgui.text("""{node.text}""")\n'
        elif isinstance(node, Button):
            label = node.label
            cb = node.callback
            render_logic += (
                f'        if imgui.button("{label}"):\n'
                f'            {cb}()\n'
            )
        elif isinstance(node, Title):
             # The h1-equivalent for the window body
            render_logic += f'        imgui.text_ansi("{node.text}")\n'
        else:
            print(f"Warning: ImGui backend does not support node type: {type(node)}")


    # --- Assemble the full code for ui.py ---
    content = f'''import sys
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer

{callback_defs}

def main():
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
