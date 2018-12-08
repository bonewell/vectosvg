from .command import Command


class PenColorCommand(Command):
    def execute(self):
        if self.params:
            color = self.params[0]
            self.adapter.pencolor(color)
