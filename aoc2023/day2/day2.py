import re
from collections import defaultdict

with open("aoc2023/day2/example.txt") as example:
    example = example.readlines()
    example_games = {}
    for line in example:
        cubes = defaultdict(list)
        spline = line.split(": ")
        id = spline[0].split(" ")[-1]
        for tri in spline[1].split("; "):
            for color in tri.split(", "):
                color = color.split()
                cubes[color[1]].append(int(color[0]))
        example_games[int(id)] = cubes

# examples[id] =

with open("aoc2023/day2/input.txt") as input:
    input = input.readlines()
    input_games = {}
    for line in input:
        cubes = defaultdict(list)
        spline = line.split(": ")
        id = spline[0].split(" ")[-1]
        for tri in spline[1].split("; "):
            for color in tri.split(", "):
                color = color.split()
                cubes[color[1]].append(int(color[0]))
        input_games[int(id)] = cubes

with open("aoc2023/day1/example2.txt") as example2:
    example2 = example2.readlines()

mapping = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

not_valid = set()
for id, game in example_games.items():
    for color in game:
        for num in game[color]:
            if num > mapping[color]:
                not_valid.add(id)
print(sum((set(example_games) - not_valid)))

not_valid = set()
for id, game in input_games.items():
    for color in game:
        for num in game[color]:
            if num > mapping[color]:
                not_valid.add(id)
# print(not_valid)
print(sum((set(input_games) - not_valid)))

sum = 0
for id, game in example_games.items():
    power = 1
    for color in game:
        power *= max(game[color])
    sum += power
print(sum)

sum = 0
for id, game in input_games.items():
    power = 1
    for color in game:
        power *= max(game[color])
    sum += power
print(sum)
