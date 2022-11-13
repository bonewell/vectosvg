from .command import Command


class AngleCommand(Command):
    def execute(self):
        a = self.params[0]
        self.adapter.rotate(a)
