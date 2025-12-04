import os
import time

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read()


def bench(part):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = part(*args, **kwargs)
        print(f"\tevaluation time: {time.perf_counter() - start} s")
        return value

    return wrapper


@bench
def part1(data=input_data):
    sum = 0
    for indentifier in data.split(","):
        first, second = map(int, indentifier.split("-"))
        for number in range(first, second + 1):
            number = str(number)
            if len(number) % 2 == 0:
                left, right = number[: len(number) // 2], number[len(number) // 2 :]
                if left == right:
                    sum += int(number)
    print(f"Part 1: {sum=}")


@bench
def part2(data=input_data):
    sum = 0
    for indentifier in data.split(","):
        first, second = map(int, indentifier.split("-"))
        for number in range(first, second + 1):
            number = str(number)
            for l in range(1, len(number) + 1):
                if len(number) % l == 0 and (z := len(number) // (l)) != 1 and (number.count(number[:l])) == z:
                    sum += int(number)
                    break
    print(f"Part 2: {sum=}")


part1(example_data)
part1(input_data)
print()
part2(example_data)
part2(input_data)
