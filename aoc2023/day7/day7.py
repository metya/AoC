import os
from collections import Counter, defaultdict

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()


def solve1(data):
    hands = {}
    cc = {}
    groups = defaultdict(list)
    ordered = []
    mapping = str.maketrans({"T": "A", "J": "B", "Q": "C", "K": "D", "A": "E"})

    for ind, line in enumerate(data):
        hand, bid = line.split()
        hands[ind] = [hand, bid]

    for i, (hand, bid) in hands.items():
        cc[i] = sorted(Counter(hand).items(), key=lambda x: (x[1]), reverse=True)

    rotveller = sorted(
        cc.items(),
        key=lambda x: (x[1][0][1], x[1][1][1]) if len(x[1]) > 1 else (x[1][0][1], 1),
        reverse=True,
    )

    for ind, rot in rotveller:
        if len(rot) == 1:
            groups[f"{rot[0][1]}"].append((ind, hands[ind]))
        else:
            groups[f"{rot[0][1]}_{rot[1][1]}"].append((ind, hands[ind]))

    for k, v in groups.items():
        s_g = sorted(v, key=lambda x: x[1][0].translate(mapping), reverse=True)
        for el in s_g:
            ordered.append((k, el))

    s = 0
    for rank, hand in zip(reversed(range(1, len(ordered) + 1)), ordered):
        k, hand = hand
        s += int(hands[hand[0]][1]) * rank

    print(s)
    return s


def solve2(data):
    hands = {}
    cc = {}
    groups = defaultdict(list)
    ordered = []
    mapping = str.maketrans({"T": "A", "J": "1", "Q": "C", "K": "D", "A": "E"})

    for ind, line in enumerate(data):
        hand, bid = line.split()
        hands[ind] = [hand, bid]

    for i, (hand, bid) in hands.items():
        c = sorted(Counter(hand).items(), key=lambda x: (x[1]), reverse=True)
        if c[0][0] == "J":
            if len(c) > 1:
                a = c[1][0]
            else:
                a = "J"
        else:
            a = c[0][0]
        cc[i] = sorted(
            Counter(hand.replace("J", a)).items(), key=lambda x: (x[1]), reverse=True
        )

    rotveller = sorted(
        cc.items(),
        key=lambda x: (x[1][0][1], x[1][1][1]) if len(x[1]) > 1 else (x[1][0][1], 1),
        reverse=True,
    )

    for ind, rot in rotveller:
        if len(rot) == 1:
            groups[f"{rot[0][1]}"].append((ind, hands[ind]))
        else:
            groups[f"{rot[0][1]}_{rot[1][1]}"].append((ind, hands[ind]))

    for k, v in groups.items():
        s_g = sorted(v, key=lambda x: x[1][0].translate(mapping), reverse=True)
        for el in s_g:
            ordered.append((k, el))

    s = 0
    for rank, hand in zip(reversed(range(1, len(ordered) + 1)), ordered):
        k, hand = hand
        s += int(hands[hand[0]][1]) * rank

    print(s)
    return s


solve1(example_data)
solve1(input_data)
solve2(example_data)
solve2(input_data)
