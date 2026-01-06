# Stencil: Generate UIs from a Single Source

## Challenge

In a world with countless UI frameworks for web, desktop, and mobile, developers spend significant time writing boilerplate code for each platform. Building the same UI across different technologies leads to duplicated effort, inconsistencies, and a slower development cycle. How can we accelerate UI prototyping and development without being tied to a single framework from the start?

## Abstract

Stencil is a lightweight command-line tool that empowers developers to generate UI code for multiple backends from a single, simple YAML configuration file. By defining the UI components once, developers can produce boilerplate code for web (HTML), desktop (ImGui), terminal (Curses), and mobile (Flutter) applications instantly. Stencil's modular architecture allows for easy extension to new frameworks, streamlining the process of UI creation and enabling rapid, cross-platform prototyping.

## Novelty

The novelty of Stencil lies in its simplicity and extensibility. Unlike complex, all-in-one development platforms, Stencil focuses on doing one thing well: generating clean, idiomatic UI code from an abstract definition. Its key innovations are:

*   **Single Source of Truth:** A simple YAML file defines the entire UI, making it easy to read, version control, and modify.
*   **Pluggable Backends:** The architecture is designed to be backend-agnostic, allowing new UI frameworks to be added with minimal effort.
*   **Framework-Native Code:** Stencil generates human-readable, framework-specific code, not a web view wrapped in a native shell. This allows developers to take the generated code and build upon it using the native tools and libraries of their chosen platform.

## Results

Stencil has proven to be an effective tool for rapid UI prototyping. Key results include:

*   **Reduced Development Time:** Drastically cuts down the time required to create initial UI mockups across multiple platforms.
*   **Consistent UIs:** Ensures that the fundamental UI structure is consistent across different backends.
*   **Flexibility:** Allows developers to experiment with different UI frameworks for their project without committing to one early on.
*   **Flutter Integration:** Successfully extended to support Flutter, demonstrating the flexibility of the backend architecture.

## Architecture Design

Stencil's architecture is a multi-stage pipeline:

1.  **UI Definition (YAML):** A user-friendly YAML file to define UI elements.
2.  **CLI:** The entry point for the user to interact with the tool.
3.  **Parser:** Reads and validates the YAML file.
4.  **Intermediate Representation (IR):** A backend-agnostic representation of the UI components.
5.  **Backend Code Generators:** Modular components that translate the IR into specific UI framework code (HTML, ImGui, Curses, Flutter).
6.  **File Output:** Generates the final source code files.

![Stencil Architecture Diagram](https://i.imgur.com/3Z3g3Z7.png)
