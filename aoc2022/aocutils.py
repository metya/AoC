import os
import requests
import bs4
import markdownify as md

def create_jl(task_dir: str, day: int):
    jl_path = os.path.join(task_dir, "puzzle.jl")
    if os.path.exists(jl_path):
        os.utime(jl_path, None)
    else:
        open(jl_path, "a").close()


def generate_readme(task_dir: str, day: int):
    os.makedirs(task_dir, exist_ok=True)
    readme_path = os.path.join(task_dir, "README.md")
    cookies_dict = {
        "session": "53616c7465645f5fefb3f3f69b82ffe6cf03aeb1a491c72b218281b2f7a8fc768b12c1f70fe183ba512239efd882d68c28426443fd2b7e71c03833bfdbdd3562"
    }

    soup = bs4.BeautifulSoup(
        requests.get(
            f"https://adventofcode.com/2022/day/{day}", cookies=cookies_dict
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

    cookies_dict = {
        "session": "53616c7465645f5f479c5542473264aed531b6c7ec141c211d7b5b73dc7e982507a8452a3f54c7c91e666d48e23dedb590e8637e3003669d5c71bc35d7a3b6cc"
    }

    os.makedirs(task_dir, exist_ok=True)

    if os.path.exists(input_path):
        with open(input_path, "r") as f:
            input = f.read().splitlines()
    else:
        input = requests.get(
            f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies_dict
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



if __name__ == "__main__":
    
    day = 6
    generate_readme(f"day{day}", day)
    get_input(f"day{day}", day)
    create_jl(f"day{day}", day)