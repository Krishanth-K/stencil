
import os
import subprocess
from .abstract_classes.Component import Component

def to_camel_case(snake_str):
    """Converts snake_case_string to CamelCaseString."""
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

class ReactBackend:
    def __init__(self, components: list[Component], output_dir: str = "output/react_app"):
        self.components = components
        self.output_dir = output_dir
        self.app_name = os.path.basename(output_dir)

    def generate(self):
        """Generates a complete React project."""
        print(f"Generating React project in {self.output_dir}...")

        # 1. Scaffold a new React + Vite + SWC project
        self._create_vite_project()

        # 2. Install Tailwind CSS
        self._setup_tailwind()

        # 3. Generate React components from stencil.yaml
        self._generate_app_jsx()

        print("\nGeneration complete!")
        print(f"To run your new React app:")
        print(f"  cd {self.output_dir}")
        print(f"  npm install")
        print(f"  npm run dev")

    def _run_command(self, command, cwd):
        """Runs a shell command in a specified directory."""
        print(f"Running command: {command} in {cwd}")
        try:
            result = subprocess.run(command, cwd=cwd, check=True, shell=True, capture_output=True, text=True)
            print("STDOUT:\n", result.stdout)
            print("STDERR:\n", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
            raise
        except subprocess.TimeoutExpired as e:
            print(f"Command timed out after {timeout} seconds")
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
            raise

    def _create_vite_project(self):
        """Creates a new Vite project."""
        if os.path.exists(self.output_dir):
            print(f"Directory {self.output_dir} already exists. Skipping Vite creation.")
            return

        parent_dir = os.path.dirname(self.output_dir)
        app_name = os.path.basename(self.output_dir)

        # Create parent directory if it doesn't exist.
        # Handles cases like 'output/my-app'
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        # The command will be run in the parent directory, or the current directory if there's no parent.
        cwd = parent_dir or "."
        
        print(f"Scaffolding Vite project '{app_name}' in '{cwd}'...")
        # Non-interactive command using `npm create vite`
        self._run_command(f"npm create vite@latest {app_name} -- --template react-swc", cwd=cwd)

    def _setup_tailwind(self):
        """Installs and configures Tailwind CSS."""
        print("Setting up Tailwind CSS...")
        # Install Tailwind CSS dependencies
        self._run_command("npm install -D tailwindcss postcss autoprefixer", cwd=self.output_dir)
        # Initialize Tailwind CSS
        self._run_command("npx tailwindcss init -p", cwd=self.output_dir)

        # Configure tailwind.config.js
        tailwind_config = f"""
/** @type {{import('tailwindcss').Config}} */
export default {{
  content: [
    "./index.html",
    "./src/**/*.{{js,ts,jsx,tsx}}",
  ],
  theme: {{
    extend: {{}},
  }},
  plugins: [],
}}
"""
        with open(os.path.join(self.output_dir, "tailwind.config.js"), "w") as f:
            f.write(tailwind_config)

        # Configure src/index.css
        index_css = """
@tailwind base;
@tailwind components;
@tailwind utilities;
"""
        with open(os.path.join(self.output_dir, "src/index.css"), "w") as f:
            f.write(index_css)

    def _generate_app_jsx(self):
        """Generates the main App.jsx file with components."""
        print("Generating React components...")
        body = []
        for component in self.components:
            component_type = component.__class__.__name__
            if component_type == "Title":
                body.append(f'<h1 className="text-4xl font-bold my-4">{component.text}</h1>')
            elif component_type == "Textbox":
                body.append(f'<p className="my-2">{component.text}</p>')
            elif component_type == "Input":
                label = getattr(component, 'label', to_camel_case(component.name))
                body.append(f'''
<div className="my-4">
    <label htmlFor="{component.name}" className="block text-sm font-medium text-gray-700">{label}</label>
    <input type="text" id="{component.name}" name="{component.name}" className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
</div>
''')
            elif component_type == "Button":
                body.append(f'<button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded my-2">{component.text}</button>')
            elif component_type == "Separator":
                body.append('<hr className="my-6" />')

        app_jsx_content = f"""
import React from 'react';

function App() {{
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md">
            {''.join(body)}
        </div>
    </div>
  );
}}

export default App;
"""
        with open(os.path.join(self.output_dir, "src/App.jsx"), "w") as f:
            f.write(app_jsx_content)

        # Overwrite the default main.jsx to ensure it's clean
        main_jsx_content = """
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
        with open(os.path.join(self.output_dir, "src/main.jsx"), "w") as f:
            f.write(main_jsx_content)
