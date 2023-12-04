import os
import jax
import jax.numpy as jnp

with open(os.path.join(os.path.abspath(""), "day3", "example.txt")) as example:
    example = example.readlines()
with open(os.path.join(os.path.abspath(""), "day3", "input.txt")) as input:
    input = input.readlines()


def solve1(pop):
    example = []
    for ind, line in enumerate(pop):
        line = "." + line.replace("\n", ".")
        example.append(line)
    example.insert(0, "." * len(example[0]))
    example.append("." * len(example[0]))

    part_numbers = []
    numbers = []
    adjacent = False
    for i in range(len(example) - 1):
        number = ""
        for j in range(len(example[0]) - 1):
            el = example[i][j]
            if example[i][j].isdigit():
                number += example[i][j]
                if (
                    example[i - 1][j - 1] != "."
                    or example[i - 1][j] != "."
                    or example[i - 1][j + 1] != "."
                    or example[i + 1][j - 1] != "."
                    or example[i + 1][j] != "."
                    or example[i + 1][j + 1] != "."
                    or not (example[i][j + 1] == "." or example[i][j + 1].isdigit())
                    or not (example[i][j - 1] == "." or example[i][j - 1].isdigit())
                ):
                    adjacent = True
            else:
                if number != "" and not adjacent:
                    numbers.append(int(number))
                    adjacent = False
                elif number and adjacent:
                    part_numbers.append(int(number))
                    adjacent = False
                number = ""
    # print(part_numbers)
    print(sum(part_numbers))
    return part_numbers


solve1(example)
a = solve1(input)

def solve2(pop):
    example = []
    for ind, line in enumerate(pop):
        line = "." + line.replace("\n", ".")
        example.append(line)
    example.insert(0, "." * len(example[0]))
    example.append("." * len(example[0]))

    part_numbers = []
    numbers = []
    gear = False
    geared = {}
    for i in range(len(example) - 1):
        number = ""
        for j in range(len(example[0]) - 1):
            el = example[i][j]
            if example[i][j].isdigit():
                number += example[i][j]
                if (
                    example[i - 1][j - 1] == "*"
                    or example[i - 1][j] == "*"
                    or example[i - 1][j + 1] == "*"
                    or example[i + 1][j - 1] == "*"
                    or example[i + 1][j] == "*"
                    or example[i + 1][j + 1] == "*"
                    or not (example[i][j + 1] == "*" or example[i][j + 1].isdigit())
                    or not (example[i][j - 1] == "*" or example[i][j - 1].isdigit())
                ):
                    gear = True
            else:
                if number != "" and not gear:
                    numbers.append(int(number))
                    gear = False
                elif number and gear:
                    part_numbers.append(int(number))
                    gear = False
                number = ""


def solve_reddit(lines):
    lines = [line.strip() for line in lines]
    NUM_LINES = len(lines)
    LINE_LEN = len(lines[0])

    nums = []
    for i in range(len(lines)):
        j = 0
        while j < LINE_LEN:
            if lines[i][j].isdecimal():
                start = j
                num = ""
                while j < LINE_LEN and lines[i][j].isdecimal():
                    num += lines[i][j]
                    j += 1
                j -= 1
                nums.append((int(num), (i, start, j)))

            j += 1

    sum = 0
    pnums = []
    for num in nums:
        part_number = False
        for i in range(num[1][0] - 1, num[1][0] + 2):
            if i >= 0 and i < NUM_LINES:
                for j in range(num[1][1] - 1, num[1][2] + 2):
                    if j >= 0 and j < LINE_LEN:
                        if not (lines[i][j].isdecimal() or lines[i][j] == "."):
                            part_number = True
                            sum += num[0]
                            pnums.append(num[0])
                            break
                if part_number:
                    break

    print(sum)
    return pnums


b = solve_reddit(input)

print([n for n in b if n not in a])
