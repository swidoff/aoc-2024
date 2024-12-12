import dataclasses


def read_input() -> list[str]:
    with open("../input/day10.txt") as f:
        return f.readlines()


@dataclasses.dataclass
class Input(object):
    grid: list[list[int]]
    trailheads: list[(int, int)]


def parse_input(lines: list[str]) -> Input:
    grid = []
    trailheads = []
    for r, line in enumerate(lines):
        row = []
        for c, ch in enumerate(line.strip()):
            n = int(ch)
            if n == 0:
                trailheads.append((r, c))
            row.append(n)
        grid.append(row)
    return Input(grid, trailheads)


def count_trails(
    grid: list[list[int]], r: int, c: int, seen: set[(int, int)] | None
) -> int:
    if seen is not None:
        if (r, c) in seen:
            return 0

        seen.add((r, c))

    n = grid[r][c]
    if n == 9:
        return 1

    res = 0
    for r_d, c_d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        new_r = r + r_d
        new_c = c + c_d
        if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]):
            if grid[new_r][new_c] == n + 1:
                res += count_trails(grid, new_r, new_c, seen)

    return res


def part1(inp: Input) -> int:
    res = 0
    for r, c in inp.trailheads:
        res += count_trails(inp.grid, r, c, set())
    return res


def part2(inp: Input) -> int:
    res = 0
    for r, c in inp.trailheads:
        res += count_trails(inp.grid, r, c, None)
    return res


example1 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1)) == 36


def test_part1():
    res = part1(parse_input(read_input()))
    print(res)
    assert res == 825


def test_part2_example():
    assert part2(parse_input(example1)) == 81


def test_part2():
    res = part2(parse_input(read_input()))
    print(res)
    assert res == 1805
