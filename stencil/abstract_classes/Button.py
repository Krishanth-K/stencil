from .Component import Component

class Button(Component):
    def __init__(self, text, **kwargs):
        self.text = text
        self.kwargs = kwargs
        # For backward compatibility with other backends
        self.label = text
        for key, value in kwargs.items():
            setattr(self, key, value)
