# advent of code day 10 by Ruma (Lynn)

with open(r'.\input\day10.txt') as file:
    data = file.read().split('\n')

def syntax_error_correction(data):
    pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
    correction_score = {')': 1, ']': 2, '}': 3, '>': 4}
    corruption_score = {')': 3, ']': 57, '}': 1197, '>': 25137}
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

    line_corruptions = []
    line_corrections = []
    for line in data:
        line = list(line)
        while line:
            try:
                correction = opengroup('')
                total = 0
                for char in correction:
                    total = total * 5 + correction_score[char]
                line_corrections.append((correction, total))
            except SyntaxError as err:
                linescore = corruption_score[str(err)[-1]]
                line_corruptions.append(linescore)
                break

    return tuple(line_corrections), sum(line_corruptions)

def solveA():
    print(syntax_error_correction(data)[1])

def solveB():
    corrections = list(syntax_error_correction(data)[0])
    corrections.sort(key=lambda x: x[1])
    median = int((len(corrections)-1)/2)
    print(corrections[median][1])
