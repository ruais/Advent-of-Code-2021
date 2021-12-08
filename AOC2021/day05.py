# advent of code day 5 by Ruma (Lynn)

class Map:
    def __init__(self, coords0 = (0, 0), coords1 = (0, 0)):
        self.array = [[[0]]]
        self.x, self.y = coords0
        self.width = lambda: len(self.array[0])
        self.height = lambda: len(self.array)
        self.range = lambda: ((self.x, self.y),
                                (self.x+self.width()-1, self.y-self.height()+1)
                                )
        self.expand(coords1)

    def expand(self, *coords):
        for x, y in coords:
            while not(self.y >= y > self.y - self.height()):
                lenx = self.width()
                leny = self.height()
                fixed = self.y >= y
                if not fixed: self.y += 1
                self.array.insert(fixed * leny, [[0] for _ in range(lenx)])

            while not(self.x <= x < self.x + self.width()):
                lenx = self.width()
                leny = self.height()
                fixed = self.x <= x
                if not fixed: self.x -= 1
                inspos = fixed * lenx
                for i in range(leny):
                    self.array[i].insert(inspos, [0])

    def pull(self, coords, dataonly = True):
        x, y = coords[0] - self.x, self.y - coords[1]
        inRange = 0 <= x < self.width() and 0 <= y < self.height()
        if inRange:
            obj = self.array[y][x]
            if dataonly: obj = obj[0]
            return obj
        else:
            return None

    def interact(self, func, *coords):
        self.expand(*coords)
        if isinstance(func, (list, tuple)):
            func, *args = func
        else:
            args = []
        for c in coords:
            c = self.pull(c, False)
            c[0] = func([c[0]] + args)

    def lineInteract(self, func, coords0, coords1):
        lenline = max(map(lambda n: abs(coords0[n] - coords1[n]) + 1, range(2)))
        pos = lambda xy, step: coords0[xy] + round(
                                step/(lenline-1) * (coords1[xy] - coords0[xy])
                                )
        line = [(pos(0, i), pos(1, i)) for i in range(lenline)]

        self.interact(func, *line)

    def squareInteract(self, func, coords0, coords1):
        x = sorted([coords0[0], coords1[0]])
        y = sorted([coords0[1], coords1[1]])
        x[1] += 1
        y[1] += 1

        square = []
        for i in range(*x):
            square += [(i, j) for j in range(*y)]

        self.interact(func, *square)

    def search(self, func = None, coords0 = None, coords1 = None):
        if not (coords0 or coords1):
            coords0, coords1 = self.range()
        x = sorted([coords0[0], coords1[0]])
        y = sorted([coords0[1], coords1[1]])
        x[1] += 1
        y[1] += 1

        finds = []
        for i in range(*x):
            for j in range(*y):
                obj = self.pull((i, j))
                if obj is not None and (not func or func(obj)):
                    finds.append(obj)

        return tuple(finds)

    def draw(self, coords0 = None, coords1 = None):
        if not (coords0 or coords1):
            coords0, coords1 = self.range()
        x = sorted([coords0[0], coords1[0]])
        y = sorted([coords0[1], coords1[1]])
        x[1] += 1
        y[1] += 1

        lines = []
        for i in range(*x):
            lines.append([self.pull((i, j)) for j in range(*y)])

        space = lambda l: max([len(str(o)) if o is not None else 0 for o in l])
        space = max(map(space, lines))
        pad = lambda string: (space-len(string)) * ' ' + string
        for y in lines:
            if not all(x is None for x in y):
                print(*[str(x) for x in y if x is not None])

import re

with open(r'.\input\day05.txt') as file:
    data = file.read()

plot = Map()

# # 5A
# for line in data.split('\n'):
#     match = re.fullmatch(r'(-?\d+),(-?\d+) -> (-?\d+),(-?\d+)', line)
#     if match:
#         x0, y0, x1, y1 = map(int, match.groups())
#         if x0 == x1 or y0 == y1:
#             plot.lineInteract((sum, 1), (x0, y0), (x1, y1))

# 5B
for line in data.split('\n'):
    match = re.fullmatch(r'(-?\d+),(-?\d+) -> (-?\d+),(-?\d+)', line)
    if match:
        x0, y0, x1, y1 = map(int, match.groups())
        plot.lineInteract((sum, 1), (x0, y0), (x1, y1))

print(len(plot.search(lambda x: x > 1)))
