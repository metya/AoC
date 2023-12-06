import os
from math import sqrt, ceil, floor

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()


def solve(times, dists):
    def root_eq(b, c):
        D = b**2 - 4 * c
        x1 = (b - sqrt(D)) / 2
        x2 = (b + sqrt(D)) / 2
        return x1, x2

    total = 1
    for time, dist in zip(times, dists):
        at_least, less_then = root_eq(time, dist)
        solution_number = ceil(less_then) - floor(at_least) - 1
        total *= solution_number
    print(total)
    return total


def parse1(data):
    times = [int(n) for n in data[0][5:].split()]
    dists = [int(n) for n in data[1][9:].split()]
    return times, dists


def parse2(data):
    times = [int(data[0][5:].replace(" ", ""))]
    dists = [int(data[1][9:].replace(" ", ""))]
    return times, dists


solve(*parse1(example_data))
solve(*parse1(input_data))
solve(*parse2(example_data))
solve(*parse2(input_data))
