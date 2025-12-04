import os
import numpy as np

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()


def part1(data):
    grid = np.array([list(w) for w in data])
    sum = 0
    grid = np.pad(grid, pad_width=((1, 1), (1, 1)), mode="constant", constant_values="_")
    H, W = grid.shape
    for i in range(H - 3 + 2):
        for j in range(W - 3 + 2):
            if grid[i, j] == "@":
                subgrid = grid[i - 1 : i + 2, j - 1 : j + 2]
                count = np.sum(subgrid == "@")
                if count < 5:
                    sum += 1

    print(f"Part 1: {sum=}")


def part2(data):
    grid = np.array([list(w) for w in data])
    sum = 0
    grid = np.pad(grid, pad_width=((1, 1), (1, 1)), mode="constant", constant_values="_")
    H, W = grid.shape
    can_remove = True
    rounds = 0
    while can_remove:
        coords2remove = []
        for i in range(H - 3 + 2):
            for j in range(W - 3 + 2):
                if grid[i, j] == "@":
                    subgrid = grid[i - 1 : i + 2, j - 1 : j + 2]
                    count = np.sum(subgrid == "@")
                    if count < 5:
                        sum += 1
                        coords2remove.append((i, j))
        if len(coords2remove) == 0:
            can_remove = False
        else:
            rounds += 1
            grid[tuple(zip(*coords2remove))] = "."

    print(f"Part 2: {sum=} after {rounds} rounds")


part1(example_data)
part1(input_data)

part2(example_data)
part2(input_data)
