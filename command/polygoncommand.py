from .command import Command


class PolygonCommand(Command):
    def execute(self):
        points = []
        for i in range(len(self.params)):
            if i % 2 == 0:
                x = self.params[i]
            else:
                y = self.params[i]
                points.append((x, y))
        self.adapter.polygon(points)
