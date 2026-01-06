# 📘 Stencil

[![PyPI version](https://badge.fury.io/py/stencil-ui.svg)](https://pypi.org/project/stencil-ui/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/stencil-ui.svg)](https://pypi.org/project/stencil-ui/)

`stencil` is a lightweight CLI tool that generates UI code for various backends from a single YAML or JSON configuration file. Describe your UI once and let `stencil` generate the boilerplate for web, desktop, or terminal applications.

---

## ✨ Features

*   **Multi-Backend Support**: Generate UIs for HTML, React (web), Flutter (mobile), ImGui (desktop), and Curses (terminal).
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

Use the `stencil` command to create your UI from the `stencil.yaml` file.

```bash
stencil
```

By default, `stencil` generates an HTML file. You can specify a different backend using the `--backend` or `-b` flag:

```bash
# Generate an HTML file
stencil -b html

# Generate a React application
stencil -b react

# Generate a Flutter application
stencil -b flutter

# Generate an ImGui desktop application
stencil -b imgui

# Generate a Curses terminal application
stencil -b curses
```

### 3. Watch for Changes

For rapid development, you can use the `--watch` flag to automatically regenerate the UI whenever you save changes to your `stencil.yaml`:

```bash
stencil --watch
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

| Element     | YAML Example                                  | HTML Output         | React Output        | Flutter Output      | ImGui Output          | Curses Output         |
|-------------|-----------------------------------------------|---------------------|---------------------|---------------------|-----------------------|-----------------------|
| `title`     | `- title: "My App"`                           | `<h1>` & `<title>`  | `<h1>`              | `Text` (headline)   | Window Title          | Centered bold text    |
| `text`      | `- text: "Hello!"`                            | `<p>`               | `<p>`               | `Text`              | `imgui.text`          | Centered text         |
| `button`    | `- button: {label: "Click", callback: "on_click"}`  | `<button>`          | `<button>`          | `ElevatedButton`    | `imgui.button`        | `[ Click ]`           |
| `separator` | `- separator`                                 | `<hr>`              | `<hr>`              | `Divider`           | `imgui.separator`     | `──────────`          |
| `input`     | `- input: {label: "Name", placeholder: "Your name"}`   | `<input type="text">` | `<input type="text">` | `TextField`         | `imgui.input_text`    | `Name: [       ]`     |

---

## 🖼 Example Outputs

Based on the configuration example above, here's what `stencil` will generate for each backend:

*   **HTML (`-b html`)**: Creates an `index.html` and `style.css` in `output/html/`.
*   **React (`-b react`)**: Generates a set of React components and an `App.tsx` file in `output/react/src`. To use this, you need a React project.
*   **Flutter (`-b flutter`)**: Creates a new Flutter project in `output/flutter_app/` and generates the `main.dart` file. Run `flutter run` in `output/flutter_app` to launch the mobile app.
*   **ImGui (`-b imgui`)**: Creates a `ui.py` file in `output/imgui/`. Run `python output/imgui/ui.py` to launch a native desktop window.
*   **Curses (`-b curses`)**: Creates a `tui.py` file in `output/curses/`. Run `python output/curses/tui.py` in your terminal to launch a text-based UI.

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