import dataclasses


def read_input() -> list[str]:
    with open("../input/day25.txt") as f:
        return [l.strip() for l in f.readlines()]


@dataclasses.dataclass
class Input(object):
    locks: list[tuple[int, ...]]
    keys: list[tuple[int, ...]]


def parse_input(lines: list[str]) -> Input:
    locks = []
    keys = []
    for i in range(0, len(lines), 8):
        schematic = lines[i : i + 7]
        heights = tuple(
            sum(line[c] == "#" for line in schematic) - 1 for c in range(0, 5)
        )
        if schematic[0][0] == "#":
            locks.append(heights)
        else:
            keys.append(heights)
    return Input(locks, keys)


def part1(inp: Input) -> int:
    res = 0
    for lock in inp.locks:
        for key in inp.keys:
            if all(l + k < 6 for l, k in zip(lock, key)):
                res += 1
    return res


example1 = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1)) == 3


def test_part1():
    res = part1(parse_input(read_input()))
    print(res)
