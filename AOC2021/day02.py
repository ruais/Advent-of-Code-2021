# advent of code day 2 by Ruma (Lynn)

with open(r'.\input\day02.txt') as file:
    data = file.read()

# # 2A
# def travel(commands):
#     from re import fullmatch
#     from functools import reduce
#     commands = [c for c in commands.split('\n') if c]
#     # axes (x, y), each with a keyword for (-, +)
#     drxns = (('BACKWARD', 'FORWARD'), ('UP', 'DOWN'))
#     coords = [0, 0]
#     for c in commands:
#         c = c.upper()
#         c = fullmatch(f"^({'|'.join(reduce(tuple.__add__, drxns))}) (\\d+)$", c)
#         if c:
#             drxn, distns = c.groups()
#             for i in range(2):
#                 if drxn in drxns[i]:
#                     heading = drxns[i].index(drxn) or -1
#                     coords[i] += heading * int(distns)
#                     break
#     return tuple(coords)

# 2B
def travel(commands):
    from re import fullmatch
    from functools import reduce
    commands = commands.split('\n')
    # axes (x, y), each with a keyword for (-, +)
    drxns = (('BACKWARD', 'FORWARD'), ('UP', 'DOWN'))
    coords = [0, 0]
    aim = 0
    for c in commands:
        c = c.upper()
        c = fullmatch(f"^({'|'.join(reduce(tuple.__add__, drxns))}) (\\d+)$", c)
        if c:
            drxn, val = c.groups()
            val = int(val)
            if drxn in drxns[0]:
                heading = drxns[0].index(drxn) or -1
                coords[0] += heading * val
                coords[1] += heading * aim * val
            else:
                aim += (drxns[1].index(drxn) or -1) * val
    return tuple(coords)

print(int.__mul__(*travel(data)))
