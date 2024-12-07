import functools
import itertools
import operator
from typing import Callable


def read_input() -> list[str]:
    with open("../input/day07.txt") as f:
        return [s.strip() for s in f.readlines()]


def parse_input(lines: list[str]) -> list[(int, list[int])]:
    res = []
    for line in lines:
        value, numbers = line.split(": ", maxsplit=1)
        res.append((int(value), [int(n) for n in numbers.split(" ")]))
    return res


def part1(inp_: list[(int, list[int])]) -> int:
    return sum(
        value
        for value, operands in inp_
        if is_solvable(operands, value, [operator.add, operator.mul])
    )


def is_solvable(
    operands: list[int], value: int, operators: list[Callable[[int, int], int]]
) -> bool:
    return any(
        functools.reduce(
            lambda r, op: op[0](r, op[1]), zip(operators, operands[1:]), operands[0]
        )
        == value
        for operators in (itertools.product(operators, repeat=len(operands) - 1))
    )


def concat(op1: int, op2: int) -> int:
    return int(str(op1) + str(op2))


def part2(inp_: list[(int, list[int])]) -> int:
    return sum(
        value
        for value, operands in inp_
        if is_solvable(operands, value, [operator.add, operator.mul])
        or is_solvable(operands, value, [operator.add, operator.mul, concat])
    )


example1 = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1)) == 3749


def test_part1():
    assert part1(parse_input(read_input())) == 66343330034722


def test_part2_example():
    assert part2(parse_input(example1)) == 11387


def test_part2():
    assert part2(parse_input(read_input())) == 637696070419031
