import os
import math

with open(os.path.join(os.path.dirname(__file__), "example.txt")) as example:
    example_data = example.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as example:
    input_data = example.read().splitlines()


def bench(part):
    import time

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = part(*args, **kwargs)
        print(f"\tevaluation time: {time.perf_counter() - start} s")
        return value

    return wrapper


def cluster_by_distance(points, max_links=None):
    """
    points: list of list shape 3
    returns cluster as a dict, each cluster – list if index of points
    """

    n = len(points)

    # collect edges/distances
    edges = []
    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            edges.append((dist, i, j))

    edges.sort(key=lambda e: e[0])
    max_links = len(edges) if not max_links else max_links

    # Union–Find (DSU)
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1
        return True

    # just walk through the edges
    links_done = 0
    for dist, i, j in edges[:max_links]:
        if union(i, j):
            last_pair = i, j
            links_done += 1

    # collect clusters
    clusters = {}
    for i in range(n):
        r = find(i)
        clusters.setdefault(r, []).append(i)

    return clusters, links_done, last_pair


def part1(data, n):
    from functools import reduce
    from operator import mul

    points = [list(map(int, point.split(","))) for point in data]
    clusters, _, _ = cluster_by_distance(points, n)
    result = reduce(mul, [len(c[1]) for c in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)[:3]])
    print(f"Part1: {result}")


@bench
def part2(data):
    points = [list(map(int, point.split(","))) for point in data]
    _, _, last_pair = cluster_by_distance(points)
    result = points[last_pair[0]][0] * points[last_pair[1]][0]
    print(f"Part2: {result}")


part1(example_data, 10)
part1(input_data, 1000)
part2(example_data)
part2(input_data)
