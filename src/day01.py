import re
from collections import Counter


def read_input() -> list[str]:
    with open("../input/day01.txt") as f:
        return f.readlines()

def parse_input(inp: list[str]) -> tuple[list[int], list[int]]:
    ls1 = []
    ls2 = []
    for line in inp:
        if line:
            num1, num2 = re.split(r"\s+", line, maxsplit=1)
            ls1.append(int(num1))
            ls2.append(int(num2))
    return ls1, ls2

def part1(ls1: list[int], ls2: list[int]) -> int:
    return sum(abs(n1 - n2) for n1, n2 in zip(sorted(ls1), sorted(ls2)))

def part2(ls1: list[int], ls2: list[int]) -> int:
    cnt2 = Counter(ls2)
    return sum(num * cnt2[num] for num in ls1)

example = """
3   4
4   3
2   5
1   3
3   9
3   3
""".splitlines()


def test_part1_example():
    assert part1(*parse_input(example)) == 11

def test_part1():
    assert part1(*parse_input(read_input())) == 1889772

def test_part2_example():
    assert part2(*parse_input(example)) == 31

def test_part2():
    assert part2(*parse_input(read_input())) == 23228917
