import sys
import json

def generate_imgui(data):
    """
    Generates a standalone Python file (ui.py) that renders an ImGui interface
    based on the provided 'data' structure.
    """
    title = data.get("title", "ImGui Window")
    app_data = data.get("app")

    if not app_data:
        print("Error: Config must have a top-level 'app' key with a list of elements")
        sys.exit(1)

    # --- Create callback stubs ---
    callback_defs = ""
    for element in app_data:
        if "button" in element:
            cb_name = element["button"]["callback"]
            callback_defs += f"""
def {cb_name}():
    print("Callback '{cb_name}' triggered")
"""

    # --- Build the ImGui rendering logic ---
    render_logic = ""
    for element in app_data:
        if "text" in element:
            render_logic += f'        imgui.text("""{element["text"]}""")\n'
        elif "button" in element:
            label = element["button"]["label"]
            cb = element["button"]["callback"]
            render_logic += (
                f'        if imgui.button("{label}"):\n'
                f'            {cb}()\n'
            )

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
{render_logic}        imgui.end()

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

    # --- Write to file ---
    # with open("ui.py", "w") as f:
    #     f.write(content)
    # print("[+] UI successfully generated -> ui.py")

    return content

