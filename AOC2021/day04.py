# advent of code day 4 by Ruma (Lynn)

class Board:
    def __init__(self, array):
        numbers = list(map(list, array))
        diagonal = [[], []]
        for i in range(len(numbers)):
            numbers[i] = tuple([n] for n in numbers[i])
            diagonal[0].append(numbers[i][i])
            diagonal[1].append(numbers[i][-i-1])
        diagonal = list(map(tuple, diagonal))

        rotated = []
        for i in range(len(numbers))[::-1]:
            rotated.append(tuple(numbers[j][i] for j in range(len(numbers))))

        self.numbers = tuple(numbers)
        self.check = tuple(numbers + diagonal + rotated)
        self.won = bool(self.checkWin())

    def checkNum(self, nextnum):
        for i in self.numbers:
            for j in i:
                if nextnum in j:
                    j[0] = -1 * j[0] - 1
                    score = (self.checkWin() or 0) * nextnum
                    if score:
                        self.won = score
                    return score or None

    def checkWin(self):
        check = map(lambda line: all(n[0] < 0 for n in line), self.check)
        if any(c for c in check):
            total = 0
            for i in self.numbers:
                for j in i:
                    if j[0] > 0: total += j[0]
            return total

with open(r'.\input\day04.txt') as file:
    data = file.read()

def parse_data(data):
    import re
    data = data.split('\n')
    calls = [int(n) for n in data.pop(0).split(',')]

    boards = []
    while data:
        line = re.findall('\d+', data.pop(0))

        if not line:
            boards.append([])
        else:
            boards[-1].append([int(n) for n in line])

    for i in range(len(boards)):
        if boards[i]:
            boards[i] = Board(boards[i])
        else:
            del boards[i]

    return boards, calls

# # 4A
# def play(boards, calls):
#     winners = []
#     while calls and not winners:
#         call = calls.pop(0)
#         for i in range(len(boards)):
#             won = boards[i].checkNum(call)
#             if won:
#                 winners.append((i, won))
#
#     winners.sort(key=lambda x: x[1], reverse = True)
#
#     return winners[0]

# 4B
def play(boards, calls):
    winners = []
    while calls:
        newwin = []
        call = calls.pop(0)
        for i in range(len(boards)):
            if not boards[i].won:
                won = boards[i].checkNum(call)
                if won:
                    newwin.append((i, won))
        winners += sorted(newwin, key=lambda x: x[1], reverse = True)

    return winners

print(play(*parse_data(data))[-1][1])
