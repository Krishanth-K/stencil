from .Component import Component


class Text(Component):
    def __init__(self, content, variant="body"):  # variant: "body", "title", "subtitle"
        super().__init__()
        self.content = content
        self.variant = variant
