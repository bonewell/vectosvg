from .command import Command


class SizeCommand(Command):
    def execute(self):
        (w, h) = self.params[0].split('x')
        self.adapter.size(w, h)
