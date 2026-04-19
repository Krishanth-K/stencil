# 📘 Stencil

[![PyPI version](https://badge.fury.io/py/stencil-ui.svg)](https://pypi.org/project/stencil-ui/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/stencil-ui.svg)](https://pypi.org/project/stencil-ui/)

**Quick throwaway UIs for developers testing logic or wrapping scripts.**

Write YAML → get a working UI in seconds. Terminal, desktop, or browser. No frontend knowledge required.

---

## Why Stencil?

You need a UI to test backend logic or wrap a script — not a production app, just something functional. Skip the boilerplate. Describe your UI once, generate it instantly.

**Backends:**
- **HTML** — browser-based, shareable
- **curses** — terminal UI, SSH-friendly
- **imgui** — desktop GUI, immediate mode

---

## Installation

```bash
pip install stencil-ui  # Python 3.12+
```

---

## Usage

```bash
stencil init              # create stencil.yaml
stencil                   # generate HTML (default)
stencil -b curses         # terminal UI
stencil -b imgui          # desktop GUI
stencil --watch           # auto-regenerate on changes
```

---

## Example Config

```yaml
config:
  backend: "html"

app:
  - title: "Task Manager"
  - input:
      label: "Task"
      placeholder: "Buy groceries..."
  - button:
      label: "Add"
      callback: "addTask"
  - separator
  - text: "© 2025"
```

**Components:** `title`, `text`, `input`, `button`, `separator`

---

## Extending

Add backends by dropping a folder in `stencil/backends/<name>/`:

```
mybackend/
  backend.yaml      # metadata
  _layout.j2        # wrapper template
  Button.j2         # component templates
  Input.j2
  Text.j2
```

No Python changes needed. Engine auto-discovers backends. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## License

MIT — use it however you want.

**Contributing?** Open an issue or PR. Easiest contribution: add a new backend for your favorite framework.
