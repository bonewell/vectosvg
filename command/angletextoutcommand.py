from .command import Command
from adapter import Point, Font, Text


class AngleTextOutCommand(Command):
    def execute(self):
        a = self.params[0]
        name = self.params[1].strip()
        size = self.params[2]
        (x, y) = self.params[3:5]
        if len(self.params) > 5:
            text = self.params[5].strip()
        else:
            text = ''
        text = text.replace(r'\n', ' ')
        self.adapter.text(Point(x, y), Text(text, Font(name, size)), float(a))
