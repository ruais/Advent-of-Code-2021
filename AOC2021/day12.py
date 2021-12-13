# advent of code day 12 by Ruma (Lynn)

from collections import deque

def init():
    with open(r'.\input\day12.txt') as file:
        data = file.read()

    rooms = {}
    for line in data.split('\n'):
        if not line: continue
        link = line.split('-')
        if link[0] not in rooms: rooms[link[0]] = ()
        if link[1] not in rooms: rooms[link[1]] = ()
        if link[1] != 'start': rooms[link[0]] += (link[1],)
        if link[0] != 'start': rooms[link[1]] += (link[0],)

    # True that a small room can still be visited twice
    paths = deque([(True, 'start')])

    return rooms, paths

def solveA():
    rooms, paths = init()

    completed_paths = deque()
    while paths:
        path = paths.pop()
        for room in rooms[path[-1]]:
            newpath = path
            if room.islower() and room in newpath:
                continue

            newpath += (room,)
            if room == 'end':
                completed_paths.append(tuple(newpath[1:]))
            else:
                paths.appendleft(newpath)

    return len(completed_paths)

def solveB():
    rooms, paths = init()

    completed_paths = deque()
    while paths:
        path = paths.pop()
        for room in rooms[path[-1]]:
            newpath = path
            if room.islower() and room in newpath:
                if newpath[0]:
                    newpath = (False,) + newpath[1:]
                else:
                    continue

            newpath += (room,)
            if room == 'end':
                completed_paths.append(tuple(newpath[1:]))
            else:
                paths.appendleft(newpath)

    return len(completed_paths)
