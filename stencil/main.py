from stencil.engine import render_app

def run(tree, config_data, args):
    """
    Orchestrates the rendering process by delegating to the unified engine.
    """
    # Determine backend with correct priority: CLI > config > default
    backend_name = args.backend or config_data.get("config", {}).get("backend", "html")
    
    # Get output directory from config if it exists
    output_dir = config_data.get("config", {}).get("output_dir")
    
    # Delegate rendering to the unified template-driven engine
    render_app(tree, backend_name, output_dir=output_dir, config_data=config_data)
