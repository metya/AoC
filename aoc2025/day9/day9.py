import os
from functools import lru_cache

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


@bench
def part1(data):
    points = [list(map(int, point.split(","))) for point in data]

    n = len(points)
    max_area = 0
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            area = (dx + 1) * (dy + 1)
            if area > max_area:
                max_area = area
    print(f"Part1: {max_area=}")


@bench
def part2(data):

    def orient(a, b, c):
        """orient of trinity points: >0 – left, <0 – right, 0 – on the same line."""
        (x1, y1), (x2, y2), (x3, y3) = a, b, c
        return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

    def on_segment(a, b, c, incl=False):
        """point on the line ab"""
        (x1, y1), (x2, y2), (x3, y3) = a, b, c
        if incl:
            return min(x1, x2) <= x3 <= max(x1, x2) and min(y1, y2) <= y3 <= max(y1, y2)
        else:
            return min(x1, x2) < x3 < max(x1, x2) and min(y1, y2) < y3 < max(y1, y2)

    def segments_intersect(p1, p2, q1, q2, incl=False):
        """either cross lines p1-p2 и q1-q2"""
        o1 = orient(p1, p2, q1)
        o2 = orient(p1, p2, q2)
        o3 = orient(q1, q2, p1)
        o4 = orient(q1, q2, p2)

        # general case
        if o1 * o2 < 0 and o3 * o4 < 0:
            return True

        # partial cases: collinearity + adjoint
        if o1 == 0 and on_segment(p1, p2, q1, incl):
            return True
        if o2 == 0 and on_segment(p1, p2, q2, incl):
            return True
        if o3 == 0 and on_segment(q1, q2, p1, incl):
            return True
        if o4 == 0 and on_segment(q1, q2, p2, incl):
            return True

        return False

    def point_in_poly(x, y, poly):
        inside = False
        n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            if orient((x1, y1), (x2, y2), (x, y)) == 0 and on_segment((x1, y1), (x2, y2), (x, y), incl=True):
                return True

            # beam to the right from point (x,y)
            if (y1 > y) != (y2 > y):
                # x-coord cross with y
                x_inter = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                if x_inter >= x:
                    inside = not inside

        return inside

    def rect_inside_polygon(p1, p2, poly, cache_func=None):
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 or y1 == y2:
            return False

        xmin, xmax = (x1, x2) if x1 < x2 else (x2, x1)
        ymin, ymax = (y1, y2) if y1 < y2 else (y2, y1)

        r0 = (xmin, ymin)
        r1 = (xmin, ymax)
        r2 = (xmax, ymax)
        r3 = (xmax, ymin)
        rect = [r0, r1, r2, r3]

        if cache_func is None:

            def cache_func(xx, yy):
                return point_in_poly(xx, yy, poly)

        def is_vertex(pt):
            return pt == p1 or pt == p2

        for xx, yy in rect:
            if not is_vertex((xx, yy)):
                if not cache_func(xx, yy):
                    return False

        # check crossing edges
        rect_edges = [(r0, r1), (r1, r2), (r2, r3), (r3, r0)]
        n = len(poly)
        for e in rect_edges:
            p_a, p_b = e
            for i in range(n):
                q_a = poly[i]
                q_b = poly[(i + 1) % n]
                if segments_intersect(p_a, p_b, q_a, q_b, False):
                    return False

        return True

    # part2
    poly = [tuple(map(int, point.split(","))) for point in data]
    alpha = 0.1
    beta = 0.1

    n = len(poly)

    xs = [x for x, _ in poly]
    ys = [y for _, y in poly]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max_x - min_x
    height = max_y - min_y

    # geometric center
    cx = sum(xs) / n
    cy = sum(ys) / n

    # turn to tuple
    poly_tuple = tuple(poly)

    @lru_cache(maxsize=None)
    def pip_cached(xx, yy):
        return point_in_poly(xx, yy, poly_tuple)

    # filter candidates
    candidates = []
    for i in range(n):
        x1, y1 = poly[i]
        for j in range(i + 1, n):
            x2, y2 = poly[j]
            dx = abs(x1 - x2) + 1
            dy = abs(y1 - y2) + 1
            if dx == 0 or dy == 0:
                continue

            # heuristic 1: take only reasonable size of sides
            if dx < alpha * width or dy < beta * height:
                continue

            # heuristic 2: points lie on the both side of center
            # in one quadrant for example
            if (x1 - cx) * (x2 - cx) > 0 and (y1 - cy) * (y2 - cy) > 0:
                continue

            area_est = dx * dy
            candidates.append((area_est, i, j))

    candidates.sort(key=lambda t: t[0], reverse=True)

    best = None  # (area, p1, p2)

    for area_est, i, j in candidates:

        p1 = poly[i]
        p2 = poly[j]
        if rect_inside_polygon(p1, p2, poly_tuple, cache_func=pip_cached):
            area = area_est
            if best is None or area > best[0]:
                best = (area, p1, p2)

    if best is None:
        return None

    area, p1, p2 = best
    result = {"area": area, "p1": p1, "p2": p2}
    print(f"Part2: {result}")


part1(example_data)
part1(input_data)

part2(example_data)
part2(input_data)
