# advent of code day 6 by Ruma (Lynn)

with open(r'.\input\day06.txt') as file:
    fish = [int(f) for f in file.read().split(',')]

# # 6A
# def fish_pop_growth(fish, birthrate, youth, term):
#     fish = list(fish)
#     for _ in range(term):
#         for i in range(len(fish[:])):
#             fish[i] -= 1
#             if fish[i] < 0:
#                 fish[i] = birthrate
#                 fish.append(birthrate + youth)
#     return len(fish)
#
# print(fish_pop_growth(fish, 6, 2, 80))

# 6B
def fish_pop_growth(data, birthrate, youth, term):
    fish = (birthrate + youth) * [0]
    for f in data:
        fish[f] += 1
    for _ in range(term):
        fish[birthrate] += fish[0]
        fish = fish[1:] + [fish[0]]
    return sum(fish)

print(fish_pop_growth(fish, 7, 2, 256))
