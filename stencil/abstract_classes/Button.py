from .Component import Component


class Button(Component):
    def __init__(self, label=None, callback=None, disabled=False, style=None):
        super().__init__()

        self.label = label if label is not None else "Label"
        self.callback = callback
        self.disabled = disabled
        self.style = style
