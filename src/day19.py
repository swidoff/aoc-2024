from functools import cache


def read_input() -> list[str]:
    with open("../input/day19.txt") as f:
        return [l.strip() for l in f.readlines()]


def parse_input(lines: list[str]) -> (list[str], list[str]):
    towels = lines[0].split(", ")
    patterns = lines[2:]
    return towels, patterns


def part1(towels: list[str], patterns: list[str]) -> int:
    @cache
    def is_possible(pattern: str) -> bool:
        if not pattern:
            return True

        for t in towels:
            if pattern.startswith(t) and is_possible(pattern[len(t) :]):
                return True

        return False

    return sum(is_possible(p) for p in patterns)


def part2(towels: list[str], patterns: list[str]) -> int:
    @cache
    def count(pattern: str) -> int:
        if not pattern:
            return 1

        return sum(count(pattern[len(t) :]) for t in towels if pattern.startswith(t))

    return sum(count(p) for p in patterns)


example1 = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""".splitlines()


def test_part1_example():
    assert part1(*parse_input(example1)) == 6


def test_part1():
    res = part1(*parse_input(read_input()))
    print(res)


def test_part2_example():
    assert part2(*parse_input(example1)) == 16


def test_part2():
    res = part2(*parse_input(read_input()))
    print(res)
