import os
import re
from collections import defaultdict
from contextlib import suppress

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().split(",")

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().split(",")


def HASH(string):
    current = 0
    for letter in string:
        current += ord(letter)
        current *= 17
        current %= 256
    return current


def solve1(data):
    s = 0
    for string in data:
        s += HASH(string)
    print(s)
    return s


def solve2(data):
    s = 0
    boxes = defaultdict(dict)
    for label in data:
        label, focal_lens = re.match(r"(^\w+).(\d+)?", label).groups()
        if focal_lens is not None:
            boxes[HASH(label)][label] = int(focal_lens)
        else:
            with suppress(KeyError):
                del boxes[HASH(label)][label]
    for box, labels in boxes.items():
        for ind, (label, fl) in enumerate(labels.items(), 1):
            s += (box + 1) * ind * fl
    print(s)
    return s


solve1(example_data)
solve1(input_data)
solve2(example_data)
solve2(input_data)
