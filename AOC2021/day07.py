# advent of code day 7 by Ruma (Lynn)

with open(r'.\input\day07.txt') as file:
    crabpos = [int(p) for p in file.read().split(',')]

# 7A
# def minimum_fuel_spend(initial):
#     initial = sorted(initial)
#     median = len(initial)/2
#     median = initial[int(median)], initial[round(median)]
#     fuel_consumed = 0
#     for pos in initial:
#         fuel_consumed += abs(pos - median[0])
#     if median[0] == median[1]: median = median[0]
#     return median, fuel_consumed

# 7B
def minimum_fuel_spend(initial):
    triangle = lambda n: n * (n+1) / 2

    prev = None
    for i in range(max(initial)) + 1):
        fuel_spend = sum(map(lambda pos: triangle(abs(pos-i)), initial))
        if prev is not None and fuel_spend >= prev:
            if fuel_spend == prev:
                i = (i-1, i)
            else:
                i -= 1

            break
        prev = fuel_spend

    return i, int(prev)

print(minimum_fuel_spend(crabpos)[1])
