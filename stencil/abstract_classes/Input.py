from .Component import Component


class Input(Component):
    is_interactive = True
    def __init__(self, label=None, placeholder=None):
        super().__init__()
        self.placeholder = placeholder if placeholder is not None else "<Placeholder>"
        self.label = label if label is not None else "<Label>"
