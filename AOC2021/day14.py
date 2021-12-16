# advent of code day 14 by Ruma (Lynn)

# from collections import deque
# 
# def init():
#     with open(r'.\input\day14.txt') as file:
#         data = file.read()
#
#     data = data.split('\n\n')
#
#     polymer = deque(data[0])
#
#     data[1] = data[1].split('\n')
#     rules = {}
#     for line in data[1]:
#         if not line: continue
#         if line[0] in rules:
#             rules[line[0]][line[1]] = line[0] + line[-1] + line[1]
#         else:
#             rules[line[0]] = {line[1]: line[0] + line[-1] + line[1]}
#
#     return polymer, rules
#
# def polymerise(polymer, rules):
#     newinstance = deque()
#
#     while True:
#         newinstance.append(polymer.popleft())
#         if not polymer: break
#         newinstance.append(rules[newinstance[-1]][polymer[0]])
#
#     return newinstance
#
# def count_els(polymer):
#     count = {}
#
#     while polymer:
#         element = polymer.popleft()
#         if element not in count: count[element] = 0
#         count[element] += 1
#
#     return count
#
# def solveA():
#     polymer, rules = init()
#
#     for _ in range(10):
#         polymer = polymerise(polymer, rules)
#
#     count = count_els(polymer)
#     count = sorted(count.items(), key = lambda n: n[1], reverse = True)
#
#     return count[0][1] - count[-1][1]

def init():
    with open(r'.\input\day14.txt') as file:
        data = file.read()

    data = data.split('\n\n')

    polymer = data[0]

    data[1] = data[1].split('\n')
    rules = {}
    for line in data[1]:
        if not line: continue
        rules[line[:1]] = line[0] + line[-1] + line[1]

    return polymer, rules

def els_in_polymer(polymer, rules, depth):
    from collections import deque

    count_at_depth = {}
    def count_line(line, final = False):
        line = deque(line)
        count = {}

        left = line.popleft()
        if final: count[left] = 1
        while line:
            right = line.popleft()
            pair = left + right
            for el in count_at_depth[pair]:
                count[el] = count.get(el, 0) + count_at_depth[pair][el]
            left = right

        return count

    # build base set of values for each pair
    for pair in rules:
        count_at_depth[pair] = {pair[1]: 1}

    # compound set for each layer of depth
    while depth > 0:
        count_at_depth = {pair: count_line(rules[pair]) for pair in rules}
        depth -= 1

    return count_line(polymer, final = True)

def solve(x):
    polymer, rules = init()

    count = els_in_polymer(polymer, rules, x)
    count = sorted(count.items(), key = lambda n: n[1], reverse = True)

    return count[0][1] - count[-1][1]

def solveA():
    return solve(10)

def solveB():
    return solve(40)
