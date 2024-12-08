import dataclasses
import itertools
from collections import defaultdict


def read_input() -> list[str]:
    with open("../input/day08.txt") as f:
        return [s.strip() for s in f.readlines()]


@dataclasses.dataclass(frozen=True)
class Input(object):
    nodes: dict[str, list[(int, int)]]
    dim: int


def parse_input(lines: list[str]) -> Input:
    nodes = defaultdict(list)
    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            if val != ".":
                nodes[val].append((r, c))
    return Input(nodes, len(lines))


def part1(inp_: Input) -> int:
    antinodes = set()
    for _node, node_locs in inp_.nodes.items():
        for (r1, c1), (r2, c2) in itertools.combinations(node_locs, 2):
            r_dist = r2 - r1
            c_dist = c2 - c1
            for ar, ac in [(r2 + r_dist, c2 + c_dist), (r1 - r_dist, c1 - c_dist)]:
                if 0 <= ar < inp_.dim and 0 <= ac < inp_.dim:
                    antinodes.add((ar, ac))
    return len(antinodes)


def part2(inp_: Input) -> int:
    antinodes = set()
    for _node, node_locs in inp_.nodes.items():
        for (r1, c1), (r2, c2) in itertools.combinations(node_locs, 2):
            r_dist = r2 - r1
            c_dist = c2 - c1

            ar = r1
            ac = c1
            while 0 <= ar < inp_.dim and 0 <= ac < inp_.dim:
                antinodes.add((ar, ac))
                ar -= r_dist
                ac -= c_dist

            ar = r2
            ac = c2
            while 0 <= ar < inp_.dim and 0 <= ac < inp_.dim:
                antinodes.add((ar, ac))
                ar += r_dist
                ac += c_dist
    return len(antinodes)


example1 = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1)) == 14


def test_part1():
    res = part1(parse_input(read_input()))
    print(res)
    assert res == 240


def test_part2_example():
    assert part2(parse_input(example1)) == 34


def test_part2():
    res = part2(parse_input(read_input()))
    print(res)
    assert res == 955
