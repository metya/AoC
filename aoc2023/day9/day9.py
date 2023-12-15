import os

# from collections import Counter, defaultdict
from itertools import pairwise

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()


def diff(seq, r=False):
    glob = []
    for x, y in pairwise(seq):
        if r:
            glob.append(x - y)
        else:
            glob.append(y - x)
    return glob


def solve(data, r=False):
    seqs = []
    for line in data:
        seqs.append([int(x) for x in line.split()])
    s = []
    for seq in seqs:
        gop = []
        gop.append(seq)
        while sum(gop[-1]) != 0:
            gop.append(diff(gop[-1], r=r))
        if r:
            s.append(sum([i[0] for i in gop]))
        else:
            s.append(sum([i[-1] for i in gop]))
    print(r := sum(s))
    return r


solve(example_data)
solve(input_data)
solve(example_data, r=True)
solve(input_data, r=True)
