import dataclasses
import functools
import heapq
import operator
import re
from itertools import product

from black.trans import defaultdict


def read_input() -> list[str]:
    with open("../input/day16.txt") as f:
        return [l.strip() for l in f.readlines()]


@dataclasses.dataclass(frozen=True)
class Input(object):
    walls: set[(int, int)]
    start: (int, int)
    end: (int, int)


def parse_input(lines: list[str]) -> Input:
    walls = set()
    start = None
    end = None
    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            if val == "#":
                walls.add((r, c))
            elif val == "S":
                start = (r, c)
            elif val == "E":
                end = (r, c)
    return Input(walls, start, end)


def part1(inp: Input) -> int:
    seen = set()
    q = [(0, inp.start, d) for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
    while q:
        dist, pos, d = heapq.heappop(q)
        if pos == inp.end:
            return dist
        if pos in seen:
            continue
        seen.add(pos)

        for new_d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dr, dc = new_d
            new_pos = (pos[0] + dr, pos[1] + dc)
            if new_pos not in inp.walls:
                heapq.heappush(
                    q, (dist + 1 + (1000 if d != new_d else 0), new_pos, new_d)
                )

    return -1


example1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

example2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""


def test_part1_example():
    assert part1(parse_input(example1.splitlines())) == 7036
    assert part1(parse_input(example2.splitlines())) == 11048


def test_part1():
    res = part1(parse_input(read_input()))
    print(res)
    assert res == 108504
