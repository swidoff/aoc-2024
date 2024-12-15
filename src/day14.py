import dataclasses
import functools
import operator
import re
from itertools import product

from black.trans import defaultdict


def read_input() -> list[str]:
    with open("../input/day14.txt") as f:
        return [l.strip() for l in f.readlines()]


def parse_input(lines: list[str]) -> list[tuple[int, int, int, int]]:
    res = []
    for line in lines:
        x, y, vx, vy = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)$", line).groups()
        res.append((int(x), int(y), int(vx), int(vy)))
    return res


def part1(
    inp: list[tuple[int, int, int, int]], dim_x: int, dim_y: int, seconds: int
) -> int:
    res = defaultdict(int)
    mid_x = dim_x // 2
    mid_y = dim_y // 2
    for x, y, vx, vy in inp:
        final_x = (x + seconds * vx) % dim_x
        final_y = (y + seconds * vy) % dim_y
        if final_x != mid_x and final_y != mid_y:
            res[(final_x < mid_x, final_y < mid_y)] += 1

    return functools.reduce(operator.mul, res.values(), 1)


def part2(
    inp: list[tuple[int, int, int, int]], dim_x: int, dim_y: int, seconds: int
) -> int:
    s = 0
    res = defaultdict(int)
    for seconds in range(seconds):
        res.clear()
        for x, y, vx, vy in inp:
            final_x = (x + seconds * vx) % dim_x
            final_y = (y + seconds * vy) % dim_y
            res[(final_x, final_y)] += 1

        if (
            sum(
                1
                for x, y in res
                if all(
                    (x + xd, y + yd) in res
                    for xd, yd in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                )
            )
            > 20
        ):
            s = seconds
            break

    print(s, "seconds")
    for y in range(dim_y):
        for x in range(dim_x):
            if (x, y) in res:
                print(res[(x, y)], end="")
            else:
                print(".", end="")
        print()
    return s


example1 = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1), 11, 7, 100) == 12


def test_part1():
    res = part1(parse_input(read_input()), 101, 103, 100)
    print(res)


def test_part2():
    res = part2(parse_input(read_input()), 101, 103, 1_000_000)
    print(res)
