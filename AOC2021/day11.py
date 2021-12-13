# advent of code day 11 by Ruma (Lynn)

class Plot:
    class Neighbour:
        def __init__(self, arg, plot):
            keywords = ('t', 'x', 'o', 's')

            surr = set()
            selfinclus = False
            minx = miny = maxx = maxy = 0

            arg = arg[2:].split('|')
            for part in arg:
                part = [coord.split(',') for coord in part.split(':')]
                assert len(part) < 3
                for j in range(len(part)):
                    if part[j][0] == 'self':
                        part[j] = [0, 0]
                        continue
                    num = part[j][0].strip(' ').strip('-').isnumeric()
                    part[j] = [int(a) if num else a.strip(' ') for a in part[j]]

                if part[0][0] in keywords:
                    assert all(len(p) == 1 for p in part)
                    kw = part[0][0]
                    reg = part[-1][0]
                    if minx > -reg: minx = -reg
                    if miny > -reg: miny = -reg
                    if maxx <= reg: maxx = reg + 1
                    if maxy <= reg: maxy = reg + 1

                    if kw == 't':
                        surr.update(set(plot.__lin__((-reg,0), (reg,0))))
                        surr.update(set(plot.__lin__((0,-reg), (0,reg))))
                    if kw == 'x':
                        surr.update(set(plot.__lin__((-reg,-reg), ( reg, reg))))
                        surr.update(set(plot.__lin__((-reg, reg), ( reg,-reg))))
                    if kw == 'o':
                        surr.update(set(plot.__lin__((-reg,-reg), ( reg,-reg))))
                        surr.update(set(plot.__lin__((-reg, reg), ( reg, reg))))
                        surr.update(set(plot.__lin__((-reg,-reg), (-reg, reg))))
                        surr.update(set(plot.__lin__(( reg,-reg), ( reg, reg))))
                    if kw == 's':
                        surr.update(set(plot.__sqr__((-reg,-reg), (reg, reg))))
                else:
                    range0, range1 = plot.__range__(part[0], part[-1])
                    if minx > range0[0]: minx = range0[0]
                    if miny > range0[1]: miny = range0[1]
                    if maxx <= range1[0]: maxx = range1[0]
                    if maxy <= range1[1]: maxy = range1[1]
                    if any(coord == [0, 0] for coord in part):
                        selfinclus = True
                    surr.update(set(plot.__lin__(part[0], part[-1])))

            if not selfinclus:
                surr -= {(0,0)}

            self.coords = surr
            self.range = ((minx, miny), (maxx, maxy))

        def __getitem__(self, index):
            return (self.coords, *self.range)[index]

    def __init__(self, init0 = (0, 0), init1 = ((0,),)):
        self.x, self.y = init0
        self.upper = lambda: (self.x, self.y)
        self.lower = lambda: (self.x+self.width()-1, self.y+self.height()-1)
        self.range = lambda: (self.upper(), self.lower())
        self.width = lambda: len(self.array[0])
        self.height = lambda: len(self.array)
        self.find = lambda x: x
        if all(isinstance(j, (list, tuple)) for j in init1):
            # build from prexisting array (init0 == least coordinates in array)
            assert all(len(j) == len(init1[0]) for j in init1)
            self.array = []
            for j in init1:
                self.array.append([[i] for i in j])
        else:
            # build from coordinates (init0, init1 == opposite corners in array)
            self.array = [[[0]]]
            self.expand(init1)

    def __getitem__(self, indexes):
        if not isinstance(indexes, (list, tuple)) or len(indexes) != 2:
            raise IndexError
        i, j = self.pos(indexes)
        if None in (i, j):
            return 0
        return self.array[j][i][0]

    def __setitem__(self, indexes, data):
        if not isinstance(indexes, (list, tuple)) or len(indexes) != 2:
            raise IndexError
        i, j = self.pos(indexes)
        if None in (i, j):
            self.mutate(data, indexes)
            return
        self.array[j][i][0] = data

    def __range__(self, coords0, coords1):
        x0, x1 = sorted([coords0[0], coords1[0]])
        y0, y1 = sorted([coords0[1], coords1[1]])
        x1 += 1
        y1 += 1

        return (x0, y0), (x1, y1)

    def __lin__(self, coords0, coords1):
        if coords0 == coords1:
            return (coords0,)
        steps = max(abs(coords0[n] - coords1[n]) for n in range(2))
        pos = lambda xy, s: coords0[xy] + round(
                                s/steps * (coords1[xy] - coords0[xy])
                                )
        line = [(pos(0, n), pos(1, n)) for n in range(steps + 1)]

        return tuple(line)

    def __sqr__(self, coords0, coords1):
        square = []
        for x in range(coords0[0], coords1[0]):
            square += [(x, y) for y in range(coords0[1], coords1[1])]

        return tuple(square)

    def expand(self, *coords):
        lenx = self.width
        leny = self.height
        map = self.array
        for x, y in coords:
            fixed = self.x <= x, self.y <= y
            while not(self.x <= x <= self.lower()[0]):
                if not fixed[0]: self.x -= 1
                inspos = fixed[0] * lenx()
                for i in range(leny()):
                    map[i].insert(inspos, [0])

            while not(self.y <= y <= self.lower()[1]):
                if not fixed[1]: self.y -= 1
                map.insert(fixed[1] * leny(), [[0] for _ in range(lenx())])

    def pos(self, coords):
        x, y = coords
        i, w = x - self.x, self.width()
        j, h = y - self.y, self.height()
        i, j = (n if 0 <= n < range else None for n, range in ((i, w), (j, h)))

        return i, j

    def parsefunc(self, f):
        args = []
        if isinstance(f, (list, tuple)) and len(f) > 0:
            func, *args = f
        else:
            func = f

        if not callable(func):
            func = lambda _, x: x
            args = [f]

        for i in range(len(args)):
            arg = args[i]
            if isinstance(arg, str) and arg.strip('\\').startswith('--'):
                if arg.startswith('\\'):
                    args[i] = arg[1:]
                else:
                    args[i] = self.Neighbour(arg, self)

        return (func,) + tuple(args)

    def pull(self, coords, data = True, args = None):
        i, j = self.pos(coords)
        if None not in (i, j):
            obj = self.array[j][i]
            if data: obj = obj[0]
        else:
            obj = None

        if args is not None: args = list(args)
        for i in range(len(args or ())):
            arg = args[i]
            if isinstance(arg, Plot.Neighbour):
                surrounds, range0, range1 = tuple(arg)
                arg = []
                for y in range(range0[1], range1[1]):
                    for x in range(range0[0], range1[0]):
                        if (x,y) in surrounds:
                            s = self.pull((coords[0]+x, coords[1]+y), data)
                            arg.append(s)

                args[i] = tuple(arg) if len(arg) > 1 else arg[0]

        if args is not None:
            if len(args) == 1 and isinstance(args[0], tuple):
                args = args[0]
            return (obj,) + tuple(args)
        else:
            return obj

    def mutate(self, alter, *coords):
        self.expand(*coords)
        alter, *args = self.parsefunc(alter)
        for c in coords:
            cargs = self.pull(c, args = args)
            self[c] = alter(*cargs)

    def mutateline(self, alter, coords0, coords1):
        self.mutate(alter, *self.__lin__(coords0, coords1))

    def mutatesquare(self, alter, coords0, coords1):
        coords0, coords1 = self.__range__(coords0, coords1)
        self.mutate(alter, *self.__sqr__(coords0, coords1))

    def search(self, coords0 = None, coords1 = None,
                    filt = None, alter = None, data = True):
        if not (coords0 or coords1):
            coords0, coords1 = self.range()
        elif not coords1:
            coords1 = coords0
        coords0, coords1 = self.__range__(coords0, coords1)

        filt, *fargs = self.parsefunc(filt or (lambda x: x is not None))
        alter, *aargs = self.parsefunc(alter or self.find)

        finds = []
        for y in range(coords0[1], coords1[1]):
            for x in range(coords0[0], coords1[0]):
                obj, *args = self.pull((x, y), data, fargs)
                if filt(*[obj] + args):
                    _, *args = self.pull((x, y), data, aargs)
                    finds.append(alter(*[obj] + args))

        return tuple(finds)

def plotmap(data):
    data = tuple(tuple(int(n) for n in l) for l in data.split('\n') if l)
    return Plot((0,0), data)

def flash(plot):
    plot.mutatesquare((int.__add__, 1), *plot.range())
    activecells = list(cells)
    flashes = 0
    while activecells:
        flashed = 0
        for i in range(len(activecells))[::-1]:
            cell = activecells[i][0]
            neighbour = activecells[i][1:]
            if cell[0] > 9:
                flashed += 1
                cell[0] = 0
                for n in neighbour:
                    if n[0] > 0: n[0] += 1
                del activecells[i]
        if flashed:
            flashes += flashed
        else:
            activecells = None

    return plot, flashes

def init():
    global cells
    with open(r'.\input\day11.txt') as file:
        data = file.read()

    plot = plotmap(data)
    cells = plot.search(data = False,
                        alter = (lambda *c: [n for n in c if n], '--o:1'))

    return plot

def solveA():
    plot = init()

    flashes = 0
    for _ in range(100):
        plot, newflashes = flash(plot)
        flashes += newflashes

    return flashes

def solveB():
    plot = init()

    steps = 0
    flashes = 0
    while flashes < plot.width() * plot.height():
        steps += 1
        plot, flashes = flash(plot)

    return steps
