from stencil.abstract_classes.Button import Button
from stencil.abstract_classes.Textbox import Textbox
from stencil.abstract_classes.Title import Title
from stencil.abstract_classes.Separator import Separator
from stencil.abstract_classes.Input import Input

def generate_curses(tree):
    if not tree:
        raise ValueError("The UI tree is empty. Nothing to generate.")

    widgets = []
    interactive_widgets = []
    callback_defs = ""

    for i, node in enumerate(tree):
        widget_info = {'type': type(node).__name__.lower()}
        if isinstance(node, Title):
            widget_info['text'] = node.text
        elif isinstance(node, Textbox):
            widget_info['text'] = node.text
        elif isinstance(node, Button):
            widget_info['label'] = node.label
            widget_info['callback'] = node.callback
            interactive_widgets.append(len(widgets))
            if node.callback not in callback_defs:
                callback_defs += f"def {node.callback}():\n    pass\n\n"
        elif isinstance(node, Input):
            widget_info['label'] = node.label
            widget_info['buffer'] = node.placeholder
            interactive_widgets.append(len(widgets))
        elif isinstance(node, Separator):
            pass
        widgets.append(widget_info)

    content = f'''
import curses
import sys

# --- Callbacks ---
{callback_defs}

# --- UI Definition ---
widgets = {widgets!r}
interactive_widgets = {interactive_widgets!r}

def main(stdscr):
    if not sys.stdout.isatty():
        print("This application must be run in a terminal.")
        sys.exit(1)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN) # Highlight
    curses.curs_set(0)

    focused_widget_idx = 0
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        y_pos = h // 2 - len(widgets) // 2

        for i, widget in enumerate(widgets):
            x_pos = w // 2
            
            is_focused = interactive_widgets.index(i) == focused_widget_idx if i in interactive_widgets else False
            
            if widget['type'] == 'title':
                stdscr.addstr(y_pos, max(0, x_pos - len(widget['text']) // 2), widget['text'], curses.A_BOLD | curses.color_pair(1))
                y_pos += 2
            elif widget['type'] == 'textbox':
                for line in widget['text'].splitlines():
                    stdscr.addstr(y_pos, max(0, x_pos - len(line) // 2), line)
                    y_pos += 1
            elif widget['type'] == 'separator':
                stdscr.addstr(y_pos, max(0, x_pos - 10), "-" * 20)
                y_pos += 1
            elif widget['type'] == 'button':
                label = "[ " + widget['label'] + " ]"
                attr = curses.color_pair(2) if is_focused else curses.A_NORMAL
                stdscr.addstr(y_pos, max(0, x_pos - len(label) // 2), label, attr)
                y_pos += 1
            elif widget['type'] == 'input':
                label = widget['label'] + ": "
                buffer = widget.get('buffer', '')
                line = label + buffer
                
                attr = curses.color_pair(2) if is_focused else curses.A_NORMAL
                stdscr.addstr(y_pos, max(0, x_pos - len(line) // 2), label)
                stdscr.addstr(y_pos, max(0, x_pos - len(line) // 2 + len(label)), buffer, attr)
                y_pos += 1

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == 9: # Tab
            focused_widget_idx = (focused_widget_idx + 1) % len(interactive_widgets)
        elif key == curses.KEY_BTAB:
            focused_widget_idx = (focused_widget_idx - 1 + len(interactive_widgets)) % len(interactive_widgets)
        elif key == 10 or key == 13: # Enter
            widget_index = interactive_widgets[focused_widget_idx]
            widget = widgets[widget_index]
            if widget['type'] == 'button':
                globals()[widget['callback']]()
                # Potentially add a visual confirmation
                stdscr.addstr(h - 1, 0, "'" + widget['label'] + "' pressed!")
                stdscr.refresh()
                curses.napms(500)
        else: # Handle text input for focused Input widget
            widget_index = interactive_widgets[focused_widget_idx]
            widget = widgets[widget_index]
            if widget['type'] == 'input':
                curses.curs_set(1)
                if key == curses.KEY_BACKSPACE or key == 127:
                    widget['buffer'] = widget['buffer'][:-1]
                elif 32 <= key <= 126:
                    widget['buffer'] += chr(key)
            else:
                curses.curs_set(0)


if __name__ == "__main__":
    curses.wrapper(main)
'''
    return content
