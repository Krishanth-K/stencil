class Component:
    """A base class for all UI components."""

    def __init__(self, is_interactive=False):
        self.is_interactive = is_interactive
