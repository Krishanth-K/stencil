# 📘 Stencil

[![PyPI version](https://badge.fury.io/py/stencil.svg)](https://pypi.org/project/stencil/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/stencil.svg)](https://pypi.org/project/stencil/)

`stencil` is a **lightweight CLI tool** that generates HTML files directly from a simple YAML or JSON configuration.
No need to manually write boilerplate HTML and CSS — just describe your UI in a config file, and `stencil` handles the rest.

---

## ✨ Features

* 📝 Define UI elements (title, text, button) in YAML or JSON.
* ⚡ Generates a ready-to-use `index.html` with clean CSS styling.
* 🖱️ Automatic JavaScript stubs for button callbacks.
* 🔎 Auto-detects config file (`stencil.yaml` or `stencil.json`) in your project root.
* ⏱️ **Hot-reload support**: automatically regenerate HTML when the config file changes (`stencil --watch`).
* 🎯 Zero setup — just install and run.

---

## 📦 Installation

```bash
pip install stencil-ui
```

> Requires Python 3.8+

---

## 🚀 Usage

### 1. Create a config file

`stencil.yaml` in your project root:

```yaml
app:
  - title: "My First Stencil Page"
  - text: "Hello, world!"
  - button:
      label: "Click Me"
      callback: "onClick"
```

### 2. Generate HTML

```bash
stencil
```

> `index.html` will be generated in your project root.

---

### 3. Optional: Hot Reload

Regenerate HTML automatically when you edit your config file:

```bash
stencil --watch
```

* Monitors `stencil.yaml` or `stencil.json`
* Automatically updates `index.html` whenever the file changes
* Optional: use a browser live-reload extension to see changes immediately

---

## 🖼 Example Output

Given the above config, Stencil produces a styled HTML page like this:

```
<title>My First Stencil Page</title>
<h1>My First Stencil Page</h1>
<p>Hello, world!</p>
<button onclick="onClick">Click Me</button>
<script>
function onClick() {
    // TODO: implement this
}
</script>
```

---

## ⚙️ Configuration

Stencil looks for either:

* `stencil.yaml`
* `stencil.json`

Supported elements:

| Element  | Example                  | Output                      |
| -------- | ------------------------ | --------------------------- |
| `title`  | `- title: "My Page"`     | `<title>` + `<h1>`          |
| `text`   | `- text: "Hello World!"` | `<p>Hello World!</p>`       |
| `button` | see example above        | `<button>` with JS callback |

---

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

Stencil was built to simplify rapid prototyping of HTML pages from configs. Perfect for:

* Mockups & quick demos
* Teaching web basics
* Auto-generating documentation UIs

---

I can also **rewrite your “Example Output” section** to include a screenshot and a small live demo snippet showing **hot reload in action**, which will make the README way more appealing for users.

Do you want me to do that next?

