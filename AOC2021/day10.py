# advent of code day 10 by Ruma (Lynn)

with open(r'.\input\day10.txt') as file:
    data = file.read().split('\n')

def syntax_corruption_score(data):
    pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
    score = {')': 3, ']': 57, '}': 1197, '>': 25137}
    def opengroup():
        match = line.pop(0)
        while True:
            if not line:
                return None
            elif line[0] in pairs.values():
                if line[0] == pairs[match]:
                    line.pop(0)
                    return True
                else:
                    raise SyntaxError(line[0])
            else:
                inner = opengroup()
                if not inner:
                    return inner

    total = 0
    for line in data:
        line = list(line)
        while line:
            try:
                opengroup()
            except SyntaxError as err:
                total += score[str(err).replace('SyntaxError: ', '')]
                break

    return total

def syntax_error_correction(data):
    pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
    score = {')': 1, ']': 2, '}': 3, '>': 4}
    def opengroup(correction):
        match = line.pop(0)
        while True:
            if not line:
                correction += pairs[match]
                return correction
            elif line[0] in pairs.values():
                if line[0] == pairs[match]:
                    line.pop(0)
                    return correction
                else:
                    raise SyntaxError(line[0])
            else:
                correction = opengroup(correction)

    line_corrections = []
    for line in data:
        line = list(line)
        while line:
            try:
                correction = opengroup('')
                total = 0
                for char in correction:
                    total = total * 5 + score[char]
                line_corrections.append((correction, total))
            except SyntaxError:
                break

    return tuple(line_corrections)

def solveA():
    print(syntax_corruption_score(data))

def solveB():
    corrections = list(syntax_error_correction(data))
    corrections.sort(key=lambda x: x[1])
    median = int((len(corrections)-1)/2)
    print(corrections[median][1])
