import re


def read_input() -> list[str]:
    with open("../input/day03.txt") as f:
        return f.readlines()


def part1(lines: list[str]) -> int:
    return sum(
        int(a) * int(b)
        for line in lines
        for a, b in (re.findall("mul\((\d+),(\d+)\)", line))
    )


def part2(lines: list[str]) -> int:
    res = 0
    enabled = True
    for line in lines:
        for instr in re.findall("mul\(\d+,\d+\)|do\(\)|don't\(\)", line):
            if instr == "do()":
                enabled = True
            elif instr == "don't()":
                enabled = False
            elif enabled:
                a, b = re.match("mul\((\d+),(\d+)\)", instr).groups()
                res += int(a) * int(b)

    return res


example1 = ["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"]


def test_part1_example():
    assert part1(example1) == 161


def test_part1():
    print(part1(read_input()))


example2 = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]


def test_part2_example():
    assert part2(example2) == 48


def test_part2():
    print(part2(read_input()))
