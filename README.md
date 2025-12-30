# 📘 Stencil

[![PyPI version](https://badge.fury.io/py/stencil.svg)](https://pypi.org/project/stencil/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/stencil.svg)](https://pypi.org/project/stencil/)

`stencil` is a **lightweight CLI tool** that generates UI across various backends (like HTML and ImGui) directly from a simple YAML or JSON configuration. It's designed to be easily adaptable to new UI toolkits and frameworks.
No need to manually write boilerplate code — just describe your UI in a config file, and `stencil` handles the rest.

---

## ✨ Features

* 📝 Define UI elements (title, text, button, input, separator) in YAML or JSON.
* ⚡ Generates a ready-to-use `index.html` with clean CSS styling.
* 🖥️ Generates standalone Python ImGui applications.
* 🧩 Features an extensible architecture for easy adaptation to new UI toolkits.
* 🖱️ Automatic JavaScript stubs for button callbacks, including interactive input handling.
* 🔎 Auto-detects config file (`stencil.yaml` or `stencil.json`) in your project root.
* ⏱️ **Hot-reload support**: automatically regenerate HTML when the config file changes (`stencil generate --watch`).
* 🎯 Zero setup — just install and run.

---

## 📦 Installation

```bash
pip install stencil-ui
```

> Requires Python 3.8+

---

## 🚀 Usage

### 1. Initialize your project

Create a default `stencil.yaml` in your current directory:

```bash
stencil init
```

This will create a `stencil.yaml` file with a commented example:

```yaml
# Stencil Configuration File
# ---
# ... (full commented default config) ...
#
# app:
#   - title: "My Awesome App"
#   - text: |
#       Welcome to Stencil!
#   - button:
#       label: "Click Me!"
#       callback: "onButtonClick"
#   - separator
#   - input:
#       label: "Your Name"
#       placeholder: "Enter your name here"
#   - button:
#       label: "Submit"
#       callback: "onSubmitName"
#   - text: "© 2025 Your Company"
```
(For the actual content, run `stencil init` in an empty directory)

### 2. Generate UI

Generate `index.html` (default) or `ui.py` based on your `stencil.yaml` config:

```bash
# Generate HTML (default backend)
stencil generate

# Or specify a backend, e.g., for an ImGui desktop app
stencil generate --backend imgui
```

> `index.html` or `ui.py` will be generated in your project root.

---

### 3. Optional: Hot Reload

Regenerate UI automatically when you edit your config file:

```bash
stencil generate --watch
```

* Monitors `stencil.yaml` or `stencil.json`
* Automatically updates `index.html` or `ui.py` whenever the file changes
* Optional: use a browser live-reload extension to see HTML changes immediately

---

## 🖼 Example Output

Stencil's generated UIs are designed to be functional and clean. Here's what you can expect with a configuration that includes a title, text, an input field, and an interactive "Submit" button:

*   **HTML Backend (`stencil generate`):** Produces a styled `index.html`. Typing into the input and clicking "Submit" will trigger a JavaScript `alert()` showing your input.
*   **ImGui Backend (`stencil generate --backend imgui`):** Produces a `ui.py` script. Running `python ui.py` will open a desktop window. Typing into the input and clicking "Submit" will print your input to the console.

---

## ⚙️ Configuration

Stencil looks for either:

* `stencil.yaml`
* `stencil.json`

Supported elements:

| Element   | Example                               | Output (HTML/ImGui)                 |
| --------- | ------------------------------------- | ----------------------------------- |
| `title`   | `- title: "My Page"`                  | `<title>`+`<h1>` / Window Title + `imgui.text_ansi` |
| `text`    | `- text: "Hello World!"`              | `<p>` / `imgui.text`                |
| `button`  | `- button: {label: "Click", cb: "my"}` | `<button>` / `imgui.button`         |
| `separator` | `- separator`                         | `<hr>` / `imgui.separator`          |
| `input`   | `- input: {label: "Name", ph: "Enter"}` | `<input type="text">` / `imgui.input_text` |

## 📂 Project Structure Example

```
my-project/
│
├── stencil.yaml
├── index.html   # generated
└── css/
    └── style.css
```

---

## 🛠 Development

Clone and install locally:

```bash
git clone https://github.com/your-username/stencil-ui.git
cd stencil-ui
pip install -e .
```

Run CLI from source:

```bash
python -m stencil --watch
```

---

## 📜 License

This project is licensed under the MIT License.

---

## 💡 Inspiration

Stencil was built to simplify rapid prototyping of UI pages from configs. Its extensible backend architecture makes it perfect for:

* Mockups & quick demos across different UI frameworks.
* Teaching UI basics with abstract component definitions.
* Auto-generating interfaces for various applications with ease.
* Rapidly adding support for new UI toolkits or frameworks.

