# file: test_imgui.py

import sys
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer


def main():
    # Initialize GLFW
    if not glfw.init():
        print("Could not initialize GLFW")
        sys.exit(1)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1280, 720, "PyImGui Test", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)


    # Initialize ImGui
    imgui.create_context()
    renderer = GlfwRenderer(window)


    # Main Loop
    while not glfw.window_should_close(window):
        glfw.poll_events()  # MUST call before imgui.new_frame()
        renderer.process_inputs()

        imgui.new_frame()

        # === Your UI ===
        imgui.begin("Hello ImGui")
        imgui.text("This is a working ImGui window!")
        if imgui.button("Click Me"):
            print("Button clicked!")
        imgui.end()
        # ==============

        # Render
        gl.glClearColor(0.1, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        renderer.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    # -------------------------------
    # 4. Cleanup
    # -------------------------------
    renderer.shutdown()
    glfw.terminate()


def get_header(title):
    if not title:
        title = "Imgui window"

    return f"""
import sys
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer


def main():
    # Initialize GLFW
    if not glfw.init():
        print("Could not initialize GLFW")
        sys.exit(1)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1280, 720, {title} None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)


    # Initialize ImGui
    imgui.create_context()
    renderer = GlfwRenderer(window)


    # Main Loop
    while not glfw.window_should_close(window):
        glfw.poll_events()  # MUST call before imgui.new_frame()
        renderer.process_inputs()

        imgui.new_frame()
    """

def get_footer():
    return """
        gl.glClearColor(0.1, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        renderer.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

        renderer.shutdown()
        glfw.terminate()
    """


def generate_imgui(data):
    title = data.get("title")

    head = get_header(title)
    foot = get_footer()

    body = ""

    return head + body + foot

# main()
