from collections import deque, defaultdict


def read_input() -> list[str]:
    with open("../input/day12.txt") as f:
        return [l.strip() for l in f.readlines()]


def find_region(start: (int, int), lines: list[str]) -> set[(int, int)]:
    start_r, start_c = start
    ch = lines[start_r][start_c]

    res = set()
    q = deque()
    q.append(start)
    while q:
        coord = q.pop()
        res.add(coord)

        r, c = coord
        for r_d, c_d in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r_n, c_n = r + r_d, c + c_d
            if (
                (r_n, c_n) not in res
                and 0 <= r_n < len(lines)
                and 0 <= c_n < len(lines[0])
                and lines[r_n][c_n] == ch
            ):
                q.append((r_n, c_n))

    return res


def find_all_regions(lines):
    regions = []
    seen = set()
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if (r, c) not in seen:
                region = find_region((r, c), lines)
                seen |= region
                regions.append(region)
    return regions


def calc_perimeter(region):
    return sum(
        1
        for r, c in region
        for r_d, c_d in ((-1, 0), (1, 0), (0, -1), (0, 1))
        if (r + r_d, c + c_d) not in region
    )


def part1(lines: list[str]) -> int:
    return sum(len(r) * calc_perimeter(r) for r in find_all_regions(lines))


def calc_sides(region):
    sides = defaultdict(list)
    for r, c in region:
        for d, r_d, c_d in (
            ("above", -1, 0),
            ("below", 1, 0),
            ("left", 0, -1),
            ("right", 0, 1),
        ):
            if (r + r_d, c + c_d) not in region:
                key = (d, r * abs(r_d) if r_d else c * abs(c_d))
                sides[key].append(r if c_d else c)

    res = 0
    for side, pieces in sides.items():
        pieces = sorted(pieces)
        gaps = sum(1 for p1, p2 in zip(pieces, pieces[1:]) if p2 - p1 > 1)
        res += 1 + gaps

    return res


def part2(lines: list[str]) -> int:
    return sum(len(r) * calc_sides(r) for r in find_all_regions(lines))


example1 = """AAAA
BBCD
BBCC
EEEC""".splitlines()

example2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""".splitlines()


example3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""".splitlines()


def test_part1_example():
    assert part1(example1) == 140
    assert part1(example2) == 772
    assert part1(example3) == 1930


def test_part1():
    res = part1(read_input())
    print(res)
    assert res == 1431440


example4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""".splitlines()

example5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""".splitlines()


def test_part2_example():
    assert part2(example1) == 80
    assert part2(example2) == 436
    assert part2(example4) == 236
    assert part2(example5) == 368


def test_part2():
    res = part2(read_input())
    print(res)
    assert res == 869070
