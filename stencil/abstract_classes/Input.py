from .Component import Component

class Input(Component):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
