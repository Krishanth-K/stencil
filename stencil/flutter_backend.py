
import os
import subprocess

class FlutterBackend:
    def __init__(self, components, output_dir="output/flutter_app"):
        self.components = components
        self.output_dir = output_dir
        self.app_name = os.path.basename(output_dir)

    def generate(self):
        """Generates a complete Flutter project."""
        print(f"Generating Flutter project in {self.output_dir}...")

        # 1. Scaffold a new Flutter project
        self._create_flutter_project()

        # 2. Generate Dart code from stencil.yaml
        self._generate_main_dart()

        print("\nGeneration complete!")
        print("To run your new Flutter app:")
        print(f"  cd {self.output_dir}")
        print("  flutter run")

    def _run_command(self, command, cwd):
        """Runs a shell command in a specified directory."""
        print(f"Running command: {command} in {cwd}")
        try:
            subprocess.run(command, cwd=cwd, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            raise

    def _create_flutter_project(self):
        """Creates a new Flutter project."""
        if os.path.exists(self.output_dir):
            print(f"Directory {self.output_dir} already exists. Skipping Flutter project creation.")
            return

        parent_dir = os.path.dirname(self.output_dir) or "."
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        print(f"Scaffolding Flutter project '{self.app_name}'...")
        self._run_command(f"flutter create {self.app_name}", cwd=parent_dir)

    def _generate_main_dart(self):
        """Generates the main.dart file with Flutter widgets."""
        print("Generating Flutter widgets...")
        widgets = []
        for component in self.components:
            comp_type = component.__class__.__name__
            # Use r-strings for Dart code to avoid issues with special characters
            text = component.text if hasattr(component, 'text') else ''
            # Sanitize text to be safely included in a Dart string literal
            dart_text = text.replace('"', r'\"').replace('\n', r'\n')

            if comp_type == "Title":
                widgets.append(f'Text(r"{dart_text}", style: Theme.of(context).textTheme.headlineMedium),')
            elif comp_type == "Textbox":
                widgets.append(f'Text(r"{dart_text}"),')
            elif comp_type == "Button":
                widgets.append(f'ElevatedButton(onPressed: () {{}}, child: Text(r"{dart_text}")),')
            elif comp_type == "Input":
                label = getattr(component, 'label', '')
                dart_label = label.replace("'", r"\'")
                widgets.append(f"""
TextField(
  decoration: InputDecoration(
    border: OutlineInputBorder(),
    labelText: r'{dart_label}',
  ),
),
""")
            elif comp_type == "Separator":
                widgets.append('const Divider(),')

        widget_str = "\n              ".join(widgets)

        main_dart_content = f"""
import 'package:flutter/material.dart';

void main() {{
  runApp(const MyApp());
}}

class MyApp extends StatelessWidget {{
  const MyApp({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: r'{self.app_name}',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const MyHomePage(),
    );
  }}
}}

class MyHomePage extends StatelessWidget {{
  const MyHomePage({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text(r'{self.app_name}'),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              {widget_str}
            ]
            .map((w) => Padding(padding: const EdgeInsets.symmetric(vertical: 8.0), child: w))
            .toList(),
          ),
        ),
      ),
    );
  }}
}}
"""
        # The main.dart file is inside the 'lib' folder
        lib_dir = os.path.join(self.output_dir, "lib")
        with open(os.path.join(lib_dir, "main.dart"), "w") as f:
            f.write(main_dart_content)
