def read_input() -> list[str]:
    with open("../input/day02.txt") as f:
        return f.readlines()


def parse_input(lines: list[str]) -> list[list[int]]:
    return [[int(n) for n in line.split(" ")] for line in lines if line]


def signum(n: int):
    return 1 if n >= 0 else -1


def is_safe(report: list[int]) -> bool:
    diffs = [l2 - l1 for l1, l2 in zip(report, report[1:])]
    diff_size_constraint = all(1 <= abs(d) <= 3 for d in diffs)
    diff_order_constraint = abs(sum(signum(d) for d in diffs)) == len(diffs)
    return diff_size_constraint and diff_order_constraint


def part1(reports: list[list[int]]) -> int:
    return sum(is_safe(r) for r in reports)


def is_tolerate_bad_level_safe(report: list[int]) -> bool:
    return is_safe(report) or any(
        is_safe(report[:i] + report[i + 1 :]) for i in range(len(report))
    )


def part2(reports: list[list[int]]) -> int:
    return sum(is_tolerate_bad_level_safe(r) for r in reports)


example = parse_input(
    """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7""".splitlines()
)


def test_part1_example():
    assert part1(example) == 2


def test_part1():
    assert part1(parse_input(read_input())) == 670


def test_part2_example():
    assert part2(example) == 4


def test_part2():
    assert part2(parse_input(read_input())) == 700
