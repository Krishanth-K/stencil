# 📘 Stencil

[![PyPI version](https://badge.fury.io/py/stencil-ui.svg)](https://pypi.org/project/stencil-ui/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/stencil-ui.svg)](https://pypi.org/project/stencil-ui/)

`stencil` is a lightweight CLI tool that generates UI code for various backends from a single YAML or JSON configuration file. Describe your UI once and let `stencil` generate the boilerplate for web, desktop, or terminal applications.

---

## ✨ Features

*   **Multi-Backend Support**: Generate UIs for HTML, ImGui (desktop), and Curses (terminal).
*   **Simple Configuration**: Define your UI with a straightforward YAML or JSON file.
*   **Extensible**: Designed to be easily adaptable to new UI toolkits and frameworks.
*   **Hot-Reload**: Automatically regenerate your UI when the configuration file changes.
*   **Zero Setup**: Install and run. It's that simple.

---

## 📦 Installation

```bash
pip install stencil-ui
```

> Requires Python 3.9+

---

## 🚀 Usage

### 1. Initialize Your Project

Create a default `stencil.yaml` in your current directory:

```bash
stencil init
```

This will give you a well-commented starting point for your UI configuration.

### 2. Generate Your UI

Use the `generate` command to create your UI from the `stencil.yaml` file.

```bash
stencil generate
```

By default, `stencil` generates an HTML file. You can specify a different backend using the `--backend` or `-b` flag:

```bash
# Generate an HTML file (index.html)
stencil generate -b html

# Generate an ImGui desktop application (ui.py)
stencil generate -b imgui

# Generate a Curses terminal application (ui.py)
stencil generate -b curses
```

### 3. Watch for Changes

For rapid development, you can use the `--watch` flag to automatically regenerate the UI whenever you save changes to your `stencil.yaml`:

```bash
stencil generate --watch
```

This is especially useful with a live-reload server for web development.

---

## ⚙️ Configuration

`stencil` looks for a `stencil.yaml` or `stencil.json` file in the current directory. Here's a simple example:

```yaml
# stencil.yaml
app:
  - title: "My App"
  - text: "Welcome to Stencil!"
  - separator
  - input:
      label: "Your Name"
      placeholder: "Enter your name"
  - button:
      label: "Submit"
      callback: "submit_name"
```

### Supported Elements

| Element     | YAML Example                                  | HTML Output         | ImGui Output          | Curses Output         |
|-------------|-----------------------------------------------|---------------------|-----------------------|-----------------------|
| `title`     | `- title: "My App"`                           | `<h1>` & `<title>`  | Window Title          | Centered bold text    |
| `text`      | `- text: "Hello!"`                            | `<p>`               | `imgui.text`          | Centered text         |
| `button`    | `- button: {label: "Click", callback: "on_click"}`  | `<button>`          | `imgui.button`        | `[ Click ]`           |
| `separator` | `- separator`                                 | `<hr>`              | `imgui.separator`     | `──────────`          |
| `input`     | `- input: {label: "Name", placeholder: "Your name"}`   | `<input type="text">` | `imgui.input_text`    | `Name: [       ]`     |

---

## 🖼 Example Outputs

Based on the configuration example above, here's what `stencil` will generate for each backend:

*   **HTML (`-b html`)**: Creates an `index.html` file with basic styling and a `main.js` file with JavaScript stubs for your callbacks.
*   **ImGui (`-b imgui`)**: Creates a `ui.py` file. Run `python ui.py` to launch a native desktop window with your UI elements. Callbacks are generated as placeholder Python functions.
*   **Curses (`-b curses`)**: Creates a `ui.py` file. Run `python ui.py` in your terminal to launch a text-based UI. Use Tab to navigate and Enter to press buttons.

---

## 🛠 Development

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/your-username/stencil.git
cd stencil
pip install -e .
```

---

## 📜 License

This project is licensed under the MIT License.
