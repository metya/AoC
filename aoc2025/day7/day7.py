import os

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()


def part1(data):
    triangle = []
    splits = 0
    triangle = [0] * len(data[0])
    for row in data:
        for i in range(len(data[0]) - 1):
            if row[i] == "S":
                triangle[i] = 1
            if row[i] == "^":
                if triangle[i] == 1:
                    triangle[i] = 0
                    splits += 1
                if triangle[i - 1] == 0:
                    triangle[i - 1] += 1
                if triangle[i + 1] == 0:
                    triangle[i + 1] += 1
    print(f"Part1: {splits=}")


def part2(data):
    triangle = [0] * len(data[0])
    for row in data:
        for i in range(len(data[0]) - 1):
            if row[i] == "S":
                triangle[i] = 1
            if row[i] == "^":
                if triangle[i] != 0:
                    triangle[i - 1] += triangle[i]
                    triangle[i + 1] += triangle[i]
                    triangle[i] = 0
    print(f"Part1: worlds={sum(triangle)}")


part1(example_data)
part1(input_data)
part2(example_data)
part2(input_data)
