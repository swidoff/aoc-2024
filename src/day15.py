import dataclasses
import functools
import operator
import re
from itertools import product

from black.trans import defaultdict


def read_input() -> list[str]:
    with open("../input/day15.txt") as f:
        return [l.strip() for l in f.readlines()]


@dataclasses.dataclass(frozen=True)
class Input(object):
    grid: dict[(int, int), str]
    start: (int, int)
    moves: list[str]


def parse_input1(lines: list[str]) -> Input:
    i = 0
    grid = {}
    start = None
    while i < len(lines):
        line = lines[i]
        if line == "":
            i += 1
            break

        for j, c in enumerate(line):
            if c == "@":
                start = (i, j)
            if c != ".":
                grid[(i, j)] = c

        i += 1

    moves = []
    for line in lines[i:]:
        moves.extend(line)

    return Input(grid, start, moves)


MOVE_MAP = {
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
    "^": (-1, 0),
}


def move_obj1(loc: (int, int), move: str, grid: dict[(int, int), str]) -> (int, int):
    dr, dc = MOVE_MAP[move]
    r, c = loc
    next_loc = ((r + dr), (c + dc))
    ch = grid[loc]

    if next_loc not in grid or (
        grid[next_loc] == "O" and move_obj1(next_loc, move, grid) != next_loc
    ):
        del grid[loc]
        grid[next_loc] = ch
        new_loc = next_loc
    else:
        new_loc = loc

    return new_loc


def part1(inp: Input) -> int:
    grid = inp.grid
    robot = inp.start
    for move in inp.moves:
        robot = move_obj1(robot, move, grid)

    return sum(100 * r + c for (r, c), ch in grid.items() if ch == "O")


def parse_input2(lines: list[str]) -> Input:
    i = 0
    grid = {}
    start = None
    while i < len(lines):
        line = lines[i]
        if line == "":
            i += 1
            break

        j = 0
        for c in line:
            if c == "@":
                start = (i, j)
                grid[(i, j)] = c
            elif c == "#":
                grid[(i, j)] = c
                grid[(i, j + 1)] = c
            elif c == "O":
                grid[(i, j)] = "["
                grid[(i, j + 1)] = "]"
            j += 2
        i += 1

    moves = []
    for line in lines[i:]:
        moves.extend(line)

    return Input(grid, start, moves)


def move_obj2(
    loc: (int, int), move: str, grid: dict[(int, int), str], no_op: bool
) -> (int, int):
    dr, dc = MOVE_MAP[move]
    r, c = loc
    next_loc = ((r + dr), (c + dc))
    ch = grid[loc]

    if next_loc not in grid:
        if not no_op:
            del grid[loc]
            grid[next_loc] = ch
        new_loc = next_loc
    elif (
        move in {"<", ">"}
        and grid[next_loc] != "#"
        and move_obj2(next_loc, move, grid, False) != next_loc
    ):
        del grid[loc]
        grid[next_loc] = ch
        new_loc = next_loc
    elif (
        move in {"^", "v"}
        and grid[next_loc] == "["
        and move_obj2(next_loc, move, grid, True) != next_loc
        and move_obj2((r + dr, c + 1), move, grid, True) != (r + dr, c + 1)
    ):
        if not no_op:
            move_obj2(next_loc, move, grid, False)
            move_obj2((r + dr, c + 1), move, grid, False)
            del grid[loc]
            grid[next_loc] = ch
        new_loc = next_loc
    elif (
        move in {"^", "v"}
        and grid[next_loc] == "]"
        and move_obj2(next_loc, move, grid, True) != next_loc
        and move_obj2((r + dr, c - 1), move, grid, True) != (r + dr, c - 1)
    ):
        if not no_op:
            move_obj2(next_loc, move, grid, False)
            move_obj2((r + dr, c - 1), move, grid, False)
            del grid[loc]
            grid[next_loc] = ch
        new_loc = next_loc
    else:
        new_loc = loc

    return new_loc


def part2(inp: Input) -> int:
    grid = inp.grid
    robot = inp.start
    for move in inp.moves:
        robot = move_obj2(robot, move, grid, False)

        dim_r = max(r for r, _ in grid)
        dim_c = max(c for _, c in grid)

        # print(move)
        # for r in range(dim_r + 1):
        #     for c in range(dim_c + 1):
        #         print(grid.get((r, c), "."), end="")
        #     print()

    return sum(100 * r + c for (r, c), ch in grid.items() if ch == "[")


example1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

example2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


def test_part1_example():
    assert part1(parse_input1(example1.splitlines())) == 2028
    assert part1(parse_input1(example2.splitlines())) == 10092


def test_part1():
    res = part1(parse_input1(read_input()))
    print(res)
    assert res == 1475249


example3 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""


def test_part2_example():
    # part2(parse_input2(example3.splitlines()))
    #
    assert part2(parse_input2(example2.splitlines())) == 9021


def test_part2():
    res = part2(parse_input2(read_input()))
    print(res)
    assert res == 1509724
