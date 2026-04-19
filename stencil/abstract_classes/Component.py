class Component:
    """A base class for all UI components."""
    
    # Metadata for the engine to collect ingredients generically
    is_interactive = False
    callback = None
