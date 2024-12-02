import os
import requests
import time
import bs4
import markdownify as md

YEAR = "2024"
session_id = "53616c7465645f5fac063ee400b29580afda85dde7a28a255d300226c59d9dc7f19e200f03ce27cd6a26f59a64ee6b6d39b155c46f7a6b90b63dcb265c37cbca"


def create_files(task_dir: str, day: int):
    go_path = os.path.join(task_dir, f"day{day}.go")
    python_path = os.path.join(task_dir, f"day{day}.py")
    if os.path.exists(go_path):
        os.utime(go_path, None)
    else:
        open(go_path, "a").close()
    if os.path.exists(python_path):
        os.utime(python_path, None)
    else:
        open(python_path, "a").close()


def generate_readme(task_dir: str, day: int):
    os.makedirs(task_dir, exist_ok=True)
    readme_path = os.path.join(task_dir, "README.md")
    cookies_dict = {"session": session_id}

    soup = bs4.BeautifulSoup(
        requests.get(
            f"https://adventofcode.com/{YEAR}/day/{day}", cookies=cookies_dict
        ).content,
        features="html.parser",
    )
    with open(readme_path, "w") as readme:
        readme.write(md.markdownify(str(soup.find_all("article")[0])))
    if len(soup.find_all("article")) > 1:
        with open(readme_path, "a") as readme:
            readme.write(md.markdownify(str(soup.find_all("article")[1])))


def get_input(task_dir: str, day: int) -> tuple[list[str], list[str]] | None:
    input_path = os.path.join(task_dir, "input.txt")
    example_path = os.path.join(task_dir, "example.txt")
    readme_path = os.path.join(task_dir, "README.md")

    cookies_dict = {"session": session_id}

    os.makedirs(task_dir, exist_ok=True)

    if os.path.exists(input_path):
        with open(input_path, "r") as f:
            input = f.read().splitlines()
    else:
        input = requests.get(
            f"https://adventofcode.com/{YEAR}/day/{day}/input", cookies=cookies_dict
        ).text
        with open(input_path, "w") as f:
            f.write(input.strip())
        input = input.splitlines()

    if os.path.exists(example_path):
        with open(example_path, "r") as e:
            example = e.read().splitlines()
    elif os.path.exists(readme_path):
        with open(example_path, "w") as e:
            with open(readme_path, "r") as r:
                example = r.read().split("\n\n```\n")[1]
            e.write(example)
            example = example.splitlines()
    else:
        print("call `generate_readme()` first!")
        return

    return input, example


def bench(part):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = part(*args, **kwargs)
        print(f"\tevaluation time: {time.perf_counter() - start} s")
        return value

    return wrapper


if __name__ == "__main__":
    day = 2
    root = os.path.dirname(__file__)
    task_dir = os.path.join(root, f"day{day}")
    generate_readme(task_dir, day)
    get_input(task_dir, day)
    create_files(task_dir, day)
