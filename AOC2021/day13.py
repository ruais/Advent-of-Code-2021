# advent of code day 13 by Ruma (Lynn)

from day11 import Plot

def init():
    with open(r'.\input\day13.txt') as file:
        data = file.read()

    plot = Plot()

    folds = []
    for line in data.split('\n'):
        if not line: continue
        if not line.startswith('fold'):
            coords = line.split(',')
            plot.mutate(1, (int(coords[0]), int(coords[1])))
        else:
            fold = line.strip('fold along ').split('=')
            folds.append((fold[0], int(fold[1])))

    return plot, tuple(folds)

def fold(plot, fold):
    folded = Plot()
    fold_y = fold[0] == 'y'

    foldline = list(plot.range())
    for i in range(2):
        coord = list(foldline[i])
        coord[fold_y] = fold[1]
        foldline[i] = coord

    mirror = [0, 0]
    mirrored = plot.Neighbour('--0,0', plot)
    while True:
        mirror[fold_y] += 2
        mirrored.coords = {tuple(mirror)}
        mirrored.range = plot.__range__(mirror)
        for coord in foldline:
            coord[fold_y] -= 1

        func = (lambda *x: tuple(n for n in x if n is not None), mirrored)
        opposites = plot.search(*foldline, filt = func, alter = func)
        if not opposites: break

        line = folded.__lin__(*foldline)
        for i in range(len(line)):
            pair = opposites[i]
            if len(pair) == 1: pair += (0,)
            folded[line[i]] = int.__or__(*pair)

    return folded

def solveA():
    plot, folds = init()

    plot = fold(plot, folds[0])
    return len(plot.search(filt = (int.__eq__, 1)))

def solveB():
    plot, folds = init()

    folds = list(folds)
    while folds:
        plot = fold(plot, folds.pop(0))

    plot.draw(alter = lambda x: '#' if x else '.')
