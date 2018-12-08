from .command import Command


class DashedCommand(Command):
    def execute(self):
        points = []
        for i in range(len(self.params)):
            if i % 2 == 0:
                x = self.params[i]
            else:
                y = self.params[i]
                points.append((x, y))
        w = 1 if (len(self.params) % 2) == 0 else self.params[-1]
        self.adapter.polyline(points, w, True)
