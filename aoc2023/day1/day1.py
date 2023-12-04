import re

with open("aoc2023/day1/example.txt") as example:
    example = example.readlines()

with open("aoc2023/day1/input.txt") as input:
    input = input.readlines()

with open("aoc2023/day1/example2.txt") as example2:
    example2 = example2.readlines()

numbers = []
for line in example:
    number = ""
    for char in line:
        if char.isdigit():
            number += char
    number = number[0] + number[-1]
    numbers.append(int(number))
print(sum(numbers))

numbers = []
for line in input:
    number = ""
    for char in line:
        if char.isdigit():
            number += char
    number = number[0] + number[-1]
    numbers.append(int(number))
print(sum(numbers))

mapping = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

numbers = []
for line in example2:
    number = {}
    for ind, char in enumerate(line):
        if char.isdigit():
            number[ind] = char
    for k, v in mapping.items():
        if k in line:
            number[line.index(k)] = v[0]
    number = sorted(number.items())
    numbers.append(int(number[0][1] + number[-1][1]))
print(sum(numbers))

numbers = []
for line in input:
    number = {}
    for ind, char in enumerate(line):
        if char.isdigit():
            number[ind] = char
    for k, v in mapping.items():
        if k in line:
            for m in re.finditer(k, line):
                number[m.start()] = v[0]
    number = sorted(number.items())
    numbers.append(int(number[0][1] + number[-1][1]))
print(sum(numbers))
