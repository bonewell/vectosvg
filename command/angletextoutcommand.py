from .command import Command
from adapter import Point


class AngleTextOutCommand(Command):
    def execute(self):
        a = self.params[0]
        font = self.params[1].strip()
        size = self.params[2]
        (x, y) = self.params[3:5]
        if len(self.params) > 5:
            text = self.params[5].strip()
        else:
            text = ''
        text = text.replace(r'\n', ' ')
        self.adapter.text(Point(x, y), text, size, font, float(a))
