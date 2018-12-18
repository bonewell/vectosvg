#!/usr/bin/env python3

from interpreter import Interpreter
from command import *


class VecInterpreter(Interpreter):
    def __init__(self, filename):
        self.f = open(filename, 'r', encoding="windows-1251")

    def __del__(self):
        self.f.close()

    @staticmethod
    def command(name, params):
        if name == 'Size' or name == 'size':
            return SizeCommand(params)
        elif name == 'Angle':
            return AngleCommand(params)
        elif name == 'PenColor':
            return PenColorCommand(params)
        elif name == 'BrushColor':
            return BrushColorCommand(params)
        elif name == 'Opaque':
            return OpaqueCommand(params)
        elif name == 'Line':
            return LineCommand(params)
        elif name == 'Dashed':
            return DashedCommand(params)
        elif name == 'Polygon':
            return PolygonCommand(params)
        elif name == 'Ellipse':
            return EllipseCommand(params)
        elif name == 'Spline':
            return SplineCommand(params)
        elif name == 'Arrow':
            return ArrowCommand(params)
        elif name == 'Stairs':
            return StairsCommand(params)
        elif name == 'AngleTextOut':
            return AngleTextOutCommand(params)
        elif name == 'TextOut':
            return TextOutCommand(params)
        elif name == 'Railway':
            return RailwayCommand(params)
        elif name == 'SpotRect':
            return SpotRectCommand(params)
        elif name == 'SpotCircle':
            return SpotCircleCommand(params)
        else:
            print('Unknown command: %s' % name)
            return None

    def next(self):
        line = self.f.readline()
        if not line:
            return None

        # print line

        tokens = line.strip().strip(',').split(' ')
        if not tokens:
            return self.next()

        name = tokens[0].strip()
        if not name or name[0] == ';':
            return self.next()

        tail = tokens[1:]
        if not tail or len(tail) == 0:
            return self.next()

        raw_params = ' '.join(tokens[1:]).split(',')
        params = []
        for p in raw_params:
            params.append(p.strip())
        # print('Name: {} - {}'.format(name, params))
        cmd = VecInterpreter.command(name, params)
        return cmd if cmd else self.next()
