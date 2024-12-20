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


def count_cheats(
    path: list[tuple[int, int]],
    cheat_length: int,
    savings: int,
) -> int:
    res = 0
    gap = savings + cheat_length
    i = 0
    j = i + gap
    while j < len(path):
        (posi_r, posi_c) = path[i]
        (posj_r, posj_c) = path[j]
        dist = abs(posi_r - posj_r) + abs(posi_c - posj_c)
        if dist <= cheat_length:
            res += 1
        i += 1
        j += 1

    return res


def part1(input_: Input, cheat_length: int, savings: int) -> int:
    path = find_path(input_)
    res = 0
    seen = set()
    for s in range(savings, len(path)):
        res += count_cheats(path, cheat_length, s)
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
    assert part1(parse_input(example1), 2, 64) == 1
    assert part1(parse_input(example1), 2, 40) == 2
    assert part1(parse_input(example1), 2, 38) == 3
    assert part1(parse_input(example1), 2, 36) == 4
    assert part1(parse_input(example1), 2, 20) == 5
    assert part1(parse_input(example1), 2, 12) == 8
    assert part1(parse_input(example1), 2, 10) == 10
    assert part1(parse_input(example1), 2, 8) == 14
    assert part1(parse_input(example1), 2, 6) == 16
    assert part1(parse_input(example1), 2, 4) == 30
    assert part1(parse_input(example1), 2, 2) == 44


def test_part1():
    res = part1(parse_input(read_input()), 2, 100)
    print(res)
    assert res == 1317


def test_part2_example():
    assert part1(parse_input(example1), 20, 76) == 3
    assert part1(parse_input(example1), 20, 74) == 7
    assert part1(parse_input(example1), 20, 72) == 22
    # assert part1(parse_input(example1), 20, 38) == 3
    # assert part1(parse_input(example1), 20, 36) == 4
    # assert part1(parse_input(example1), 20, 20) == 5
    # assert part1(parse_input(example1), 20, 12) == 8
    # assert part1(parse_input(example1), 20, 10) == 10
    # assert part1(parse_input(example1), 20, 8) == 14
    # assert part1(parse_input(example1), 20, 6) == 16
    # assert part1(parse_input(example1), 20, 4) == 30
    # assert part1(parse_input(example1), 20, 2) == 44


#
#
# def test_part2():
#     res = part2(parse_input(read_input()), 100)
#     print(res)
