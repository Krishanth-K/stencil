import json
import os
from pathlib import Path


def generate_react(tree, output_dir="my_react_app/src"):
    if not tree:
        raise ValueError("The UI tree is empty. Nothing to generate.")

    app_dir = Path(output_dir)
    components_dir = app_dir / "components"
    os.makedirs(components_dir, exist_ok=True)

    component_imports = []
    generated_component_types = set()

    # First pass: Generate individual React component files and collect imports
    for component in tree:
        comp_type = component.__class__.__name__
        if comp_type == "Title" and "Title" not in generated_component_types:
            with open(components_dir / "Title.tsx", "w") as f:
                f.write(
                    """import React from 'react';

interface TitleProps {
  text: string;
}

const Title: React.FC<TitleProps> = ({ text }) => {
  return <h1 className=\"stencil-title\">{text}</h1>;
};

export default Title;
"""
                )
            generated_component_types.add("Title")
            component_imports.append("import Title from './components/Title';")

        elif comp_type == "Textbox" and "Textbox" not in generated_component_types:
            with open(components_dir / "Textbox.tsx", "w") as f:
                f.write(
                    """import React from 'react';

interface TextboxProps {
  text: string;
}

const Textbox: React.FC<TextboxProps> = ({ text }) => {
  return <p className=\"stencil-text\">{text}</p>;
};

export default Textbox;
"""
                )
            generated_component_types.add("Textbox")
            component_imports.append("import Textbox from './components/Textbox';")

        elif comp_type == "Button" and "Button" not in generated_component_types:
            with open(components_dir / "Button.tsx", "w") as f:
                f.write(
                    """import React from 'react';

interface ButtonProps {
  label: string;
  onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({ label, onClick }) => {
  return <button className=\"stencil-button\" onClick={onClick}>{label}</button>;
};

export default Button;
"""
                )
            generated_component_types.add("Button")
            component_imports.append("import Button from './components/Button';")

        elif comp_type == "Input" and "Input" not in generated_component_types:
            with open(components_dir / "Input.tsx", "w") as f:
                f.write(
                    """import React, { useState } from 'react';

interface InputProps {
  label: string;
  placeholder?: string;
}

const Input: React.FC<InputProps> = ({ label, placeholder }) => {
  const [value, setValue] = useState('');
  return (
    <div className=\"stencil-input-group\">
      <label className=\"stencil-label\">{label}</label>
      <input 
        type="text" 
        className=\"stencil-input\"
        placeholder={placeholder} 
        value={value} 
        onChange={(e) => setValue(e.target.value)} 
      />
    </div>
  );
};

export default Input;
"""
                )
            generated_component_types.add("Input")
            component_imports.append("import Input from './components/Input';")

        elif comp_type == "Separator" and "Separator" not in generated_component_types:
            with open(components_dir / "Separator.tsx", "w") as f:
                f.write(
                    """import React from 'react';

const Separator: React.FC = () => {
  return <hr className=\"stencil-separator\" />;
};

export default Separator;
"""
                )
            generated_component_types.add("Separator")
            component_imports.append("import Separator from './components/Separator';")

    # Second pass: Populate component_renders with all instances
    component_renders = []
    for component in tree:
        comp_type = component.__class__.__name__
        if comp_type == "Title":
            component_renders.append(f"<Title text={json.dumps(component.text)} />")
        elif comp_type == "Textbox":
            component_renders.append(f"<Textbox text={json.dumps(component.text)} />")
        elif comp_type == "Button":
            # callback_name = getattr(component, "callback", "undefined")
            # component_renders.append(
            # f'<Button label={json.dumps(component.label)} onClick={{() => console.log("{callback_name} clicked")}}> </Button>'
            # )
            component_renders.append(f"<Button label={json.dumps(component.label)} />")
        elif comp_type == "Input":
            placeholder = getattr(component, "placeholder", "")
            component_renders.append(
                f"<Input label={json.dumps(component.label)} placeholder={json.dumps(placeholder)} />"
            )
        elif comp_type == "Separator":
            component_renders.append("<Separator />")

    # Build import strings
    imports_string = "\n".join(sorted(list(set(component_imports))))
    renders_string = "\n      ".join(component_renders)

    # --- Generate App.tsx ---
    app_content_template = """import React from 'react';
import './index.css';
{imports_placeholder}

function App() {{
  return (
    <div className="App stencil-container">
      {renders_placeholder}
    </div>
  );
}}

export default App;
"""
    app_content = app_content_template.format(imports_placeholder=imports_string, renders_placeholder=renders_string)
    with open(app_dir / "App.tsx", "w") as f:
        f.write(app_content)

    # --- Generate a basic CSS file for general styling ---
    css_content = """\n.stencil-container {\n    font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif;\n    background-color: #f0f2f5;\n    color: #1c1e21;\n    padding: 2rem;\n    border-radius: 8px;\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.1);\n    max-width: 400px;\n    margin: 2rem auto;\n    box-sizing: border-box;\n}\n
.stencil-title {\n    font-size: 2rem;\n    color: #1877f2;\n    margin-bottom: 1.5rem;\n}\n
.stencil-text {\n    font-size: 1rem;\n    line-height: 1.5;\n    margin-bottom: 1rem;\n}\n
.stencil-button {\n    width: 100%;\n    padding: 0.8rem;\n    border: none;\n    border-radius: 6px;\n    background-color: #1877f2;\n    color: #ffffff;\n    font-size: 1.1rem;\n    font-weight: 600;\n    cursor: pointer;\n    margin-top: 1rem;\n}\n
.stencil-button:hover {\n    background-color: #166fe5;\n}\n
.stencil-separator {\n    border: 0;\n    height: 1px;\n    background-color: #dadde1;\n    margin: 1.5rem 0;\n}\n
.stencil-input-group {\n    margin-bottom: 1rem;\n}\n
.stencil-label {\n    display: block;\n    margin-bottom: 0.5rem;\n    color: #606770;\n    font-size: 0.9rem;\n    font-weight: 600;\n}\n
.stencil-input {\n    width: 100%;\n    padding: 0.8rem;\n    border: 1px solid #ccd0d5;\n    border-radius: 6px;\n    font-size: 1rem;\n    box-sizing: border-box;\n}\n
.stencil-input:focus {\n    outline: none;\n    border-color: #1877f2;\n    box-shadow: 0 0 0 2px #e7f3ff;\n}\n"""
    with open(app_dir / "index.css", "w") as f:
        f.write(css_content)

    print(f"React files generated in '{output_dir}' directory.")
