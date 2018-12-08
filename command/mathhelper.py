import math


def translate(x1, y1, x2, y2, t):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        z = -1 if dy < 0 else 1
        tx = 0
        ty = t * z
    elif dy == 0:
        z = -1 if dx < 0 else 1
        tx = t * z
        ty = 0
    else:
        a = math.atan2(dx, dy)
        tx = t * math.sin(a)
        ty = t * math.cos(a)
    return tx, ty


def is_crossed(x, t, g):
    if t > 0:
        return x > g
    else:
        return x < g
