# Contributing to Stencil

Thanks for your interest in contributing! The easiest way to contribute is by adding support for a new backend.

---

## Adding a New Backend

Each backend lives in `stencil/backends/<name>/` and consists of:

1. **`backend.yaml`** — manifest file
2. **`_layout.j2`** — outer wrapper template
3. **Component templates** — one `.j2` file per component

### 1. Create `backend.yaml`

```yaml
name: "mybackend"
default_output_dir: "output/mybackend"
output_filename: "app.ext"
copy_files:
  - style.css  # optional extra files to copy
```

### 2. Write Component Templates

Create a `.j2` file for each component: `Button.j2`, `Input.j2`, `Text.j2`, `Title.j2`, `Separator.j2`

**Template Rules:**

- **No conditionals for default values** — the component class already handles them. Just use `{{ variable }}` directly.
- **Use `tojson` for strings** — prevents syntax errors from newlines and special characters: `{{ text | tojson }}`
- **Only use conditionals for optional attributes** — like `{% if disabled %}disabled{% endif %}` for boolean flags.
- **Keep templates dumb** — no logic, just rendering. Backend-specific decisions go in the template, data logic stays in the component class.

**Example `Button.j2` (HTML):**

```html
<button
    onclick="{{ callback }}()"
    {% if disabled %}disabled{% endif %}
    style="{{ style }}"
    class="stencil-button"
>{{ label }}</button>
```

**Example `Button.j2` (curses):**

```python
{'type': 'button', 'label': {{ label | tojson }}, 'callback': {{ callback | tojson }}}
```

### 3. Write `_layout.j2`

The layout template receives:

- `body_elements` — list of rendered component strings
- `title` — app title
- `app_name` — name from config
- `callbacks` — list of unique callback names
- `input_fields` — list of input field dicts
- `interactive_widgets` — list of interactive component indices
- `config` — raw config data

**Use `loop.last` for separators:**

```jinja
widgets = [
    {% for element in body_elements %}
    {{ element }}{% if not loop.last %},{% endif %}
    {% endfor %}
]
```

**Example `_layout.j2` (HTML):**

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        {% for element in body_elements %}
        {{ element }}
        {% endfor %}
    </div>
    <script>
        {% for callback in callbacks %}
        function {{ callback }}() {
            console.log("{{ callback }} called");
        }
        {% endfor %}
    </script>
</body>
</html>
```

### 4. Test Your Backend

```bash
stencil -b mybackend
```

That's it. No Python code changes needed.

---

## Adding a New Component

1. **Create the class** in `stencil/abstract_classes/`

```python
from .Component import Component

class MyComponent(Component):
    def __init__(self, label, value=""):
        super().__init__()
        self.label = label
        self.value = value
```

2. **Add to `COMPONENT_MAP`** in `cli.py`

```python
COMPONENT_MAP = {
    "mycomponent": MyComponent,
    ...
}
```

3. **Add `.j2` template** to every existing backend

Done. The engine will automatically pick it up.

---

## Component Class Guidelines

- **Explicit attributes** — use explicit parameters, not `**kwargs` with `setattr`
- **Compute derived values in `__init__`** — don't rely on `get_context()` unless absolutely necessary
- **No backend-specific logic** — the class should work for all backends
- **Mark interactive components** — set `is_interactive = True` for buttons and inputs

**Example:**

```python
class Input(Component):
    is_interactive = True
    
    def __init__(self, label="Field", placeholder=""):
        super().__init__()
        self.label = label
        self.placeholder = placeholder
        self.safe_id = label.lower().replace(' ', '_')  # computed once
```

---

## General Guidelines

- **Keep it simple** — Stencil is for throwaway UIs, not production apps
- **Stay backend-agnostic** — abstract classes should never reference HTML, curses, or imgui specifics
- **Test across backends** — if you add a component, make sure all three backends handle it
- **Document edge cases** — if a backend can't support something, document it in the template as a comment

---

## Submitting Changes

1. Fork the repo
2. Create a feature branch (`git checkout -b add-gtk-backend`)
3. Test your changes (`stencil -b yourbackend`)
4. Commit with clear messages
5. Open a PR with a description of what you added

---

## Questions?

Open an issue or start a discussion. We're here to help.
