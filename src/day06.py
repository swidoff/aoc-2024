import dataclasses
from collections import defaultdict, Counter
from dataclasses import dataclass


def read_input() -> list[str]:
    with open("../input/day06.txt") as f:
        return [s.strip() for s in f.readlines()]


@dataclasses.dataclass(frozen=True)
class Input(object):
    hashes: set[(int, int)]
    start: (int, int)
    dim: int


def parse_input(lines: list[str]) -> Input:
    dim = len(lines[0])
    hashes = set()
    start = None
    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            if ch == "#":
                hashes.add((row, col))
            elif ch == "^":
                start = (row, col)

    return Input(hashes, start, dim)


dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class LoopException(Exception):
    pass


def guard_path(inp_: Input) -> set[(int, int)]:
    (pos_r, pos_c) = inp_.start
    dir_i = 0

    visited = defaultdict(set)
    while 0 <= pos_r < inp_.dim and 0 <= pos_c < inp_.dim:
        if dir_i in visited[(pos_r, pos_c)]:
            raise LoopException()

        visited[(pos_r, pos_c)].add(dir_i)

        (dir_r, dir_c) = dirs[dir_i]
        next_r, next_c = pos_r + dir_r, pos_c + dir_c
        if (next_r, next_c) in inp_.hashes:
            dir_i = (dir_i + 1) % len(dirs)
        else:
            pos_r, pos_c = next_r, next_c

    return visited.keys()


def part1(inp_: Input) -> int:
    return len(guard_path(inp_))


def part2(inp_: Input) -> int:
    path = guard_path(inp_)

    res = 0
    for r in range(inp_.dim):
        for c in range(inp_.dim):
            if (r, c) == inp_.start or (r, c) not in path:
                continue

            new_hash = inp_.hashes.copy()
            new_hash.add((r, c))
            new_inp = dataclasses.replace(inp_, hashes=new_hash)
            try:
                part1(new_inp)
            except LoopException:
                res += 1

    return res


example1 = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1)) == 41


#
def test_part1():
    # print(part1(parse_input(read_input())))
    assert part1(parse_input(read_input())) == 5212


def test_part2_example():
    assert part2(parse_input(example1)) == 6


def test_part2():
    # print(part2(parse_input(read_input())))
    assert part2(parse_input(read_input())) == 1767
