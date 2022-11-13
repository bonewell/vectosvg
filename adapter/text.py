from .font import Font


class Text:
    def __init__(self, string, font):
        assert isinstance(font, Font)
        self.string = string
        self.font = font
