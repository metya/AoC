import os

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()


dial = 50
zero_times = 0


def part1(data=example_data):
    dial = 50
    zero_times = 0
    for instruction in data:
        direction, amount = instruction[0], int(instruction[1:])
        if direction == "R":
            dial = (dial + amount) % 100
        elif direction == "L":
            dial = (dial - amount) % 100
        if dial == 0:
            zero_times += 1
    print(f"{dial=}, {zero_times=}")


part1(example_data)
part1(input_data)


def part2(data=example_data):
    dial = 50
    zero_times = 0
    cross_zero_times = 0
    was_zero = False

    for instruction in data:
        direction, amount = instruction[0], int(instruction[1:])
        if amount > 100:
            cross_zero_times += amount // 100
            amount = amount % 100
        if direction == "R":
            dial = dial + amount
            if dial > 100:
                cross_zero_times += 1
        elif direction == "L":
            dial = dial - amount
            if dial < 0 and not was_zero:
                cross_zero_times += 1
        dial = dial % 100
        if dial == 0:
            zero_times += 1
            was_zero = True
        else:
            was_zero = False

    print(f"{dial=}, {zero_times=}, {cross_zero_times=}, {zero_times + cross_zero_times=}")


part2(example_data)
part2(input_data)
