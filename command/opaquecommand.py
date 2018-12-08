from .command import Command


class OpaqueCommand(Command):
    def execute(self):
        self.adapter.opaque(self.params[0])
        self.adapter.pencolor('000000')
