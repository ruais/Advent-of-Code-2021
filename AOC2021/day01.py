# advent of code day 1 by Ruma (Lynn)

with open(r'.\input\day01.txt') as file:
    data = file.read()

# # 1A
# def depth(measures):
#     measures = [m for m in measures.split('\n') if m]
#     increase_decrease = [0, 0]
#     for i in range(1, len(measures)):
#         compare = (int(measures[i]), int(measures[i-1]))
#         if not int.__eq__(*compare):
#             increase_decrease[int.__lt__(*compare)] += 1
#     return tuple(increase_decrease)

# 1B
def depth_change(measures, window_size):
    measures = [m for m in measures.split('\n') if m]
    increase_decrease = [0, 0]
    i = 0
    grouped = lambda i: sum(map(int, measures[i:i+window_size]))
    while i + window_size < len(measures):
        compare = (grouped(i), grouped(i+1))
        if not int.__eq__(*compare):
            increase_decrease[int.__gt__(*compare)] += 1
        i += 1
    return tuple(increase_decrease)

print(depth_change(data, 3)[0])
