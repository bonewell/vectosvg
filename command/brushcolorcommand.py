from .command import Command


class BrushColorCommand(Command):
    def execute(self):
        if self.params:
            color = self.params[0]
            self.adapter.brushcolor(color)
