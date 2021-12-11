# advent of code day 9 by Ruma (Lynn)

from day05 import Map

def plotmap(data):
    data = data.split('\n')
    height = []
    for line in data:
        if line:
            height.append([int(n) for n in line])
    plot = Map()
    for i in range(len(height)):
        for j in range(len(height[0])):
            plot.interact((lambda _, x: x, height[i][j]), (i, j))
    return plot

def findlows(plot):
    width, height = plot.width(), plot.height()
    for i in range(width):
        for j in range(height):
            point = plot.search(None, (i, j))[0]
            search = ()
            for n in (-1, 1):
                search += plot.search(None, (i+n, j))
                search += plot.search(None, (i, j+n))

            if all(point < int(adjacent) for adjacent in search):
                plot.interact(lambda low: str(low), (i, j))

def findbasins(plot):
    def markbasin(i, coords):
        x, y = coords
        basinsize = 1
        plot.interact(lambda x: -1 * int(x) - 1, (x, y))

        for n in (-1, 1):
            neighbour = plot.search((lambda a, b, c: c > a > b, i, 9), (x+n, y))
            if neighbour:
                basinsize += markbasin(neighbour[0], (x+n, y))
            neighbour = plot.search((lambda a, b, c: c > a > b, i, 9), (x, y+n))
            if neighbour:
                basinsize += markbasin(neighbour[0], (x, y+n))

        return basinsize

    findlows(plot)
    width, height = plot.width(), plot.height()
    basins = []
    for i in range(width):
        for j in range(height):
            point = plot.search((isinstance, str), (i, j))
            if point:
                basins.append(((i, j), markbasin(int(point[0]), (i, j))))

    return tuple(basins)


def init():
    global data, plot
    with open(r'.\input\day09.txt') as file:
        data = file.read()

    plot = plotmap(data)

def solveA():
    init()

    findlows(plot)
    sum_risklevel = sum(map(lambda x: int(x)+1, plot.search((isinstance, str))))
    print(sum_risklevel)

def solveB():
    from functools import reduce
    init()

    basins = list(findbasins(plot))
    basins.sort(key=lambda basin: basin[1], reverse = True)
    print(reduce(lambda x, y: x * y, [size for coords, size in basins[:3]]))
