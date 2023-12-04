import os
from itertools import accumulate
from collections import defaultdict

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()

import time


def bench(part):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = part(*args, **kwargs)
        print(f"\tevaluation time: {time.perf_counter() - start} s")
        return value

    return wrapper


@bench
def solve1(data):
    total_points = 0
    for line in data:
        line = line.split(": ")[-1]
        have, win = line.split("|")
        have = [int(n) for n in have.split()]
        win = [int(n) for n in win.split()]
        try:
            *_, points = accumulate(
                (1 for _ in have if _ in win), func=lambda x, _: x * 2
            )
        except Exception:
            points = 0
        total_points += points
    print(total_points)


solve1(example_data)
solve1(input_data)


@bench
def solve2(data):
    cards = defaultdict(lambda: 1)
    for ind, line in enumerate(data):
        cards[ind + 1]
        line = line.split(": ")[-1]
        have, win = line.split("|")
        have = [int(n) for n in have.split()]
        win = [int(n) for n in win.split()]
        mat = sum((1 for _ in have if _ in win))
        for card in range(ind + 2, ind + 2 + mat):
            cards[card] += cards[ind + 1]
    print(sum(cards.values()))


solve2(example_data)
solve2(input_data)
