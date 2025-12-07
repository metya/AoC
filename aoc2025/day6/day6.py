import os

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()


def part1(data):
    problems = []
    for problem in data[:-1]:
        problems.append([int(d) for d in problem.split()])
    mo = data[-1].split()
    sum = 0
    for row in range(len(mo)):
        sp = 1 if mo[row] == "*" else 0
        for problem in problems:
            sp = sp * problem[row] if mo[row] == "*" else sp + problem[row]
        sum += sp
    print(f"Part1: {sum=}")


def bench(part):
    import time

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = part(*args, **kwargs)
        print(f"\tevaluation time: {time.perf_counter() - start} s")
        return value

    return wrapper


@bench
def part2(data):
    # get the max numer of tens in each colums
    mo = data[-1].split()
    tens = [list(map(len, row.split())) for row in data[:-1]]
    max_tens = []
    for i in range(len(mo)):
        pipi = []
        for ten in tens:
            pipi.append(ten[i])
        max_tens.append(max(pipi))

    # get the numbers in colums with respect of tens and position of digits
    cursor = 0
    problems = []
    for tens in max_tens:
        digits = []
        for problem in data[:-1]:
            digits.append((problem[cursor : cursor + tens]))
        problems.append(digits)
        cursor += tens + 1

    # get the result calculating digits in column with respect of tens
    sum = 0
    for problem, m in zip(problems, mo):
        sp = 1 if m == "*" else 0
        for i in range(len(problem[0])):
            num = ""
            for nums in problem:
                digit = nums[i]
                num += digit
            if m == "*":
                sp = sp * int(num)
            else:
                sp = sp + int(num)
        sum += sp
    print(f"Part2: {sum=}")


part1(example_data)
part1(input_data)

part2(example_data)
part2(input_data)
