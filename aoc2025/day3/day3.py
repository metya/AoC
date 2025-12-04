import os
import time

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()

def bench(part):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = part(*args, **kwargs)
        print(f"\tevaluation time: {time.perf_counter() - start} s")
        return value

    return wrapper


def part1(data=input_data):
    sum = 0
    for battery in data:
        jolts = [int(d) for d in battery]
        d = max(jolts)
        md = str(d)
        i = jolts.index(d)
        left, right = jolts[:i], jolts[i + 1 :]
        lmd = str(max(left)) if left != [] else ""
        rmd = str(max(right)) if right != [] else ""
        sum += int(lmd + md) if int(lmd + md) > int(md + rmd) else int(md + rmd)
    print(f"Part 1: {sum=}")


# can be used for part 1 with number_digits=2
def part2(data=input_data, number_digits=2):
    sum = 0
    for battery in data:
        jolts = [int(d) for d in battery]
        numind = []
        window_ind = len(jolts) + 1 - number_digits
        ind = 0
        for _ in range(number_digits):
            win = jolts[ind:window_ind]
            max_value = max(win)
            max_ind = win.index(max_value)
            numind.append(max_value)
            ind += max_ind + 1
            window_ind = window_ind + 1
        sum += int("".join([str(d) for d in numind]))
    print(f"Part 2: {sum=}")



part1(example_data)
part1(input_data)

part2(example_data, 12)
part2(input_data, 12)
