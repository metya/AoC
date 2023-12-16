import os
import sys
from collections import Counter
from itertools import chain

sys.setrecursionlimit(5000)

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()
    example_data = [list(n) for n in example_data]

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()
    input_data = [list(n) for n in input_data]


def init(data):
    charged = [["."] * len(data[0]) for _ in range(len(data))]
    direction = [["."] * len(data[0]) for _ in range(len(data))]
    return data, charged, direction


data, charged, direction = init(example_data)


def bounce(i=0, j=0, succ=1, h=True, v=False):
    if i >= len(data[0]) or i < 0 or j >= len(data) or j < 0:
        return
    if h:
        if succ > 0 and direction[i][j] == ">":
            return
        elif succ > 0:
            direction[i][j] = ">"
        if succ < 0 and direction[i][j] == "<":
            return
        elif succ < 0:
            direction[i][j] = "<"
    else:
        if succ > 0 and direction[i][j] == "v":
            return
        elif succ > 0:
            direction[i][j] = "v"
        if succ < 0 and direction[i][j] == "^":
            return
        elif succ < 0:
            direction[i][j] = "^"

    symbol = data[i][j]
    charged[i][j] = "#"

    if h:
        if symbol == "." or symbol == "-":
            bounce(i=i, j=j + succ, succ=succ, h=True, v=False)
        elif symbol == "|":
            bounce(i=i + succ, j=j, succ=succ, h=False, v=True)
            bounce(i=i - succ, j=j, succ=-succ, h=False, v=True)
        elif symbol == "\\":
            bounce(i=i + succ, j=j, succ=succ, h=False, v=True)
        elif symbol == "/":
            bounce(i=i - succ, j=j, succ=-succ, h=False, v=True)
        else:
            raise Exception("PIDOR GNOY " + symbol)
    elif v:
        if symbol == "." or symbol == "|":
            bounce(i=i + succ, j=j, succ=succ, h=False, v=True)
        elif symbol == "\\":
            bounce(i=i, j=j + succ, succ=succ, h=True, v=False)
        elif symbol == "/":
            bounce(i=i, j=j - succ, succ=-succ, h=True, v=False)
        elif symbol == "-":
            bounce(i=i, j=j + succ, succ=succ, h=True, v=False)
            bounce(i=i, j=j - succ, succ=-succ, h=True, v=False)
        else:
            raise Exception("PIDOR GNOY " + symbol)
    else:
        raise Exception(f"PIDOR GNOY + {h} + {v}")


# part 1 1
data, charged, direction = init(example_data)
bounce()
print(c := Counter(chain(*charged))["#"])
# part 1 2
data, charged, direction = init(input_data)
bounce()
print(c := Counter(chain(*charged))["#"])

# part 2 1
m = 0
for i in range(len(data)):
    data, charged, direction = init(example_data)
    bounce(i=i, j=0, succ=1, h=True, v=False)
    m = max(m, Counter(chain(*charged))["#"])
    data, charged, direction = init(example_data)
    bounce(i=i, j=len(data[0]) - 1, succ=-1, h=True, v=False)
    m = max(m, Counter(chain(*charged))["#"])
for j in range(len(data[0])):
    data, charged, direction = init(example_data)
    bounce(i=0, j=j, succ=1, h=False, v=True)
    m = max(m, Counter(chain(*charged))["#"])
    data, charged, direction = init(example_data)
    bounce(i=len(data) - 1, j=j, succ=-1, h=False, v=True)
    m = max(m, Counter(chain(*charged))["#"])
print(m)

# part 2 2
m = 0
for i in range(len(data)):
    data, charged, direction = init(input_data)
    bounce(i=i, j=0, succ=1, h=True, v=False)
    m = max(m, Counter(chain(*charged))["#"])
    data, charged, direction = init(input_data)
    bounce(i=i, j=len(data[0]) - 1, succ=-1, h=True, v=False)
    m = max(m, Counter(chain(*charged))["#"])
for j in range(len(data[0])):
    data, charged, direction = init(input_data)
    bounce(i=0, j=j, succ=1, h=False, v=True)
    m = max(m, Counter(chain(*charged))["#"])
    data, charged, direction = init(input_data)
    bounce(i=len(data) - 1, j=j, succ=-1, h=False, v=True)
    m = max(m, Counter(chain(*charged))["#"])
print(m)
