# 📘 Stencil

[![PyPI version](https://badge.fury.io/py/stencil.svg)](https://pypi.org/project/stencil/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/stencil.svg)](https://pypi.org/project/stencil/)

`stencil` is a **lightweight CLI tool** that generates HTML files directly from a simple YAML or JSON configuration.
No need to manually write boilerplate HTML and CSS — just describe your UI in a config file, and `stencil` handles the rest.

---

## ✨ Features

* 📝 Define UI elements (`title`, `text`, `button`) in **YAML** or **JSON**.
* ⚡ Generates a **ready-to-use `index.html`** with clean CSS styling.
* 🖱️ Automatic **JavaScript stubs** for button callbacks.
* 🔎 Auto-detects config file (`stencil.yaml` or `stencil.json`) in your project root.
* 🎯 Zero setup — just install and run.

---

## 📦 Installation

```bash
pip install stencil
```

*(requires Python 3.8+)*

---

## 🚀 Usage

1. Create a `stencil.yaml` in your project root:

```yaml
app:
  - title: "My First Stencil Page"
  - text: "Hello, world!"
  - button:
      label: "Click Me"
      callback: "onClick"
```

2. Run the CLI:

```bash
stencil
```

3. That’s it! 🎉 `index.html` will be generated in your project root.

---

## 🖼 Example Output

Given the above config, Stencil produces a styled HTML page like this:

![screenshot](https://via.placeholder.com/800x400?text=Stencil+Demo+Page)

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
git clone https://github.com/your-username/stencil.git
cd stencil
pip install -e .
```

Run CLI from source:

```bash
python -m stencil
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 💡 Inspiration

Stencil was built to simplify rapid prototyping of HTML pages from configs.
Perfect for:

* Mockups & quick demos
* Teaching web basics
* Auto-generating documentation UIs
