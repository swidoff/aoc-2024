import dataclasses
from functools import cache


def read_input() -> list[str]:
    with open("../input/day20.txt") as f:
        return [l.strip() for l in f.readlines()]


@dataclasses.dataclass
class Input(object):
    walls: set[tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]
    dim: int


def parse_input(lines: list[str]) -> Input:
    walls = set()
    start = None
    end = None
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == "#":
                walls.add((r, c))
            elif ch == "S":
                start = (r, c)
            elif ch == "E":
                end = (r, c)
    return Input(walls, start, end, len(lines))


def find_path(input_: Input) -> list[tuple[int, int]]:
    pos = input_.start
    path = [pos]
    while pos != input_.end:
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (pos[0] + dr, pos[1] + dc)
            if new_pos not in input_.walls and new_pos not in path:
                pos = new_pos
                break

        path.append(pos)

    return path


def cheat_savings(path: list[tuple[int, int]], cheat_r: int, cheat_c: int) -> int:
    adjacent_indexes = []
    for i, (r, c) in enumerate(path):
        if abs(cheat_r - r) + abs(cheat_c - c) == 1:
            adjacent_indexes.append(i)

    if len(adjacent_indexes) >= 2:
        savings = adjacent_indexes[-1] - adjacent_indexes[0] - 1
    else:
        savings = -1

    return savings


def part1(input_: Input, threshold: int) -> int:
    path = find_path(input_)

    res = 0
    for wall_r, wall_c in input_.walls:
        savings = cheat_savings(path, wall_r, wall_c)
        if savings >= threshold:
            res += 1

    return res


example1 = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1), 64) == 1
    assert part1(parse_input(example1), 40) == 2
    assert part1(parse_input(example1), 38) == 3
    assert part1(parse_input(example1), 36) == 4
    assert part1(parse_input(example1), 2) == 44


def test_part1():
    res = part1(parse_input(read_input()), 100)
    print(res)
    assert res == 1317
