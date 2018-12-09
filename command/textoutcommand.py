from .command import Command
from adapter import Point


class TextOutCommand(Command):
    def execute(self):
        font = self.params[0].strip()
        size = self.params[1]
        (x, y) = self.params[2:4]
        text = self.params[4].strip()
        text = text.replace(r'\n', ' ')
        self.adapter.text(Point(x, y), text, size, font, 0)
