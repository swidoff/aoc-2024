import dataclasses
import heapq


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


def part2(inp: Input) -> int:
    seen = {}
    best_score = None
    best_spots = set()

    q = [(0, inp.start, d, {inp.start}) for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
    while q:
        score, pos, d, path = heapq.heappop(q)
        if pos == inp.end:
            if best_score is None:
                best_score = score
                best_spots = path
            elif score == best_score:
                best_spots.update(path)
            else:
                return len(best_spots)
        if seen.get((pos, d), 1e10) < score:
            continue
        seen[(pos, d)] = score

        for new_d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dr, dc = new_d
            new_pos = (pos[0] + dr, pos[1] + dc)
            if new_pos not in inp.walls:
                new_path = set(path)
                new_path.add(new_pos)
                new_score = score + 1 + (1000 if d != new_d else 0)
                heapq.heappush(q, (new_score, new_pos, new_d, new_path))

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


def test_part2_example():
    assert part2(parse_input(example1.splitlines())) == 45
    assert part2(parse_input(example2.splitlines())) == 64


def test_part2():
    res = part2(parse_input(read_input()))
    print(res)
    assert res == 538
