import os

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()


def parse_data(data):
    ranges = []
    ing_ids = []
    for range in data:
        if "-" in range:
            start, end = map(int, range.split("-"))
            ranges.append((start, end))
        elif range == "":
            continue
        else:
            ing_ids.append(int(range))
    return ranges, ing_ids


def part1(data):
    ranges, ing_ids = parse_data(data)

    sum = 0
    for ing_id in ing_ids:
        for start, end in ranges:
            if start <= ing_id <= end:
                sum += 1
                break

    print(f"Part 1: {sum=}")


def part2(data):
    ranges, _ = parse_data(data)

    ranges.sort()
    merged = []
    current_start, current_end = ranges[0]

    for start, end in ranges[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end

    merged.append((current_start, current_end))
    sum = 0
    for start, end in merged:
        sum += end - start + 1

    print(f"Part 2: {sum=}")


part1(example_data)
part1(input_data)
part2(example_data)
part2(input_data)
