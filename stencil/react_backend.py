import os
from pathlib import Path

def generate_react(tree, output_dir="output/react/src"):
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
                f.write("""
import React from 'react';

interface TitleProps {
  text: string;
}

const Title: React.FC<TitleProps> = ({ text }) => {
  return <h1 className=\"stencil-title\">{text}</h1>;
};

export default Title;
""")
            generated_component_types.add("Title")
            component_imports.append("import Title from './components/Title';")

        elif comp_type == "Textbox" and "Textbox" not in generated_component_types:
            with open(components_dir / "Textbox.tsx", "w") as f:
                f.write("""
import React from 'react';

interface TextboxProps {
  text: string;
}

const Textbox: React.FC<TextboxProps> = ({ text }) => {
  return <p className=\"stencil-text\">{text}</p>;
};

export default Textbox;
""")
            generated_component_types.add("Textbox")
            component_imports.append("import Textbox from './components/Textbox';")
            
        elif comp_type == "Button" and "Button" not in generated_component_types:
            with open(components_dir / "Button.tsx", "w") as f:
                f.write("""
import React from 'react';

interface ButtonProps {
  label: string;
  onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({ label, onClick }) => {
  return <button className=\"stencil-button\" onClick={onClick} >{label}</button>;
};

export default Button;
""")
            generated_component_types.add("Button")
            component_imports.append("import Button from './components/Button';")

        elif comp_type == "Input" and "Input" not in generated_component_types:
            with open(components_dir / "Input.tsx", "w") as f:
                f.write("""
import React, { useState } from 'react';

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
""")
            generated_component_types.add("Input")
            component_imports.append("import Input from './components/Input';")

        elif comp_type == "Separator" and "Separator" not in generated_component_types:
            with open(components_dir / "Separator.tsx", "w") as f:
                f.write("""
import React from 'react';

const Separator: React.FC = () => {
  return <hr className=\"stencil-separator\" />;
};

export default Separator;
""")
            generated_component_types.add("Separator")
            component_imports.append("import Separator from './components/Separator';")
    
    # Second pass: Populate component_renders with all instances
    component_renders = []
    for component in tree:
        comp_type = component.__class__.__name__
        if comp_type == "Title":
            component_renders.append(f'<Title text={component.text!r} />')
        elif comp_type == "Textbox":
            component_renders.append(f'<Textbox text={component.text!r} />')
        elif comp_type == "Button":
            callback_name = getattr(component, "callback", "undefined")
            js_function = f"() => console.log('{callback_name} clicked')"
            
            # Construct onclick_attr using .format()
            onclick_attr = 'onClick={{ {} }}'.format(js_function)
            
            # Use simple string concatenation for the entire render line
            render_line = '<Button label=' + repr(component.label) + ' ' + onclick_attr + ' />'
            component_renders.append(render_line)
        elif comp_type == "Input":
            component_renders.append(f'<Input label={component.label!r} placeholder={component.placeholder!r} />')
        elif comp_type == "Separator":
            component_renders.append(f'<Separator />')

    # Build import strings
    imports_string = "\n".join(sorted(list(set(component_imports))))
    renders_string = "\n      ".join(component_renders)

    # --- Generate App.tsx ---
    app_content_template = """
import React from 'react';
import './index.css'; // Assuming you'll have a main CSS file for global styles
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
    app_content = app_content_template.format(
        imports_placeholder=imports_string,
        renders_placeholder=renders_string
    )
    with open(app_dir / "App.tsx", "w") as f:
        f.write(app_content)
    
    # --- Generate a basic CSS file for general styling ---
    css_content = """
.stencil-container {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: #f0f2f5;
    color: #1c1e21;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    margin: 2rem auto;
    box-sizing: border-box;
}

.stencil-title {
    font-size: 2rem;
    color: #1877f2;
    margin-bottom: 1.5rem;
}

.stencil-text {
    font-size: 1rem;
    line-height: 1.5;
    margin-bottom: 1rem;
}

.stencil-button {
    width: 100%;
    padding: 0.8rem;
    border: none;
    border-radius: 6px;
    background-color: #1877f2;
    color: #ffffff;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    margin-top: 1rem;
}

.stencil-button:hover {
    background-color: #166fe5;
}

.stencil-separator {
    border: 0;
    height: 1px;
    background-color: #dadde1;
    margin: 1.5rem 0;
}

.stencil-input-group {
    margin-bottom: 1rem;
}

.stencil-label {
    display: block;
    margin-bottom: 0.5rem;
    color: #606770;
    font-size: 0.9rem;
    font-weight: 600;
}

.stencil-input {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ccd0d5;
    border-radius: 6px;
    font-size: 1rem;
    box-sizing: border-box;
}

.stencil-input:focus {
    outline: none;
    border-color: #1877f2;
    box-shadow: 0 0 0 2px #e7f3ff;
}
"""
    with open(app_dir / "index.css", "w") as f:
        f.write(css_content)

    print(f"React files generated in '{output_dir}' directory.")
