import dataclasses
import heapq


def read_input() -> list[str]:
    with open("../input/day17.txt") as f:
        return [l.strip() for l in f.readlines()]


@dataclasses.dataclass(frozen=True)
class Input(object):
    a: int
    b: int
    c: int
    program: list[(int, int)]
    codes: list[str]


def parse_input(lines: list[str]) -> Input:
    a = int(lines[0].split(": ")[1])
    b = int(lines[1].split(": ")[1])
    c = int(lines[2].split(": ")[1])
    raw_program = lines[4].split(": ")[1]
    codes = raw_program.split(",")
    program = [(int(codes[i]), int(codes[i + 1])) for i in range(0, len(codes), 2)]
    return Input(a, b, c, program, codes)


def run_program(inp_: Input, a_override: int | None = None) -> str:
    a = a_override if a_override is not None else inp_.a
    b = inp_.b
    c = inp_.c
    out = []

    def combo(v):
        if 0 <= v <= 3:
            return v
        elif v == 4:
            return a
        elif v == 5:
            return b
        elif v == 6:
            return c

    i = 0
    program = inp_.program
    while i < len(program):
        (op, arg) = program[i]
        if op == 0:
            a = int(a / 2 ** combo(arg))
        elif op == 1:
            b = b ^ arg
        elif op == 2:
            b = combo(arg) % 8
        elif op == 3 and a != 0:
            i = arg
            continue
        elif op == 4:
            b = b ^ c
        elif op == 5:
            out.append(str(combo(arg) % 8))
        elif op == 6:
            b = int(a / 2 ** combo(arg))
        elif op == 7:
            c = int(a / 2 ** combo(arg))
        i += 1

    return ",".join(out)


def part1(inp_: Input) -> str:
    return run_program(inp_)


def search(a: int, i: 0, inp: Input) -> int:
    if i == len(inp.codes):
        return a

    res = None
    for remainder in range(8):
        expected = ",".join(inp.codes[-(i + 1) :])
        new_a = a * 8 + remainder
        actual = run_program(inp, new_a)
        if actual == expected:
            new_a = search(new_a, i + 1, inp)
            if new_a is not None:
                res = min(res or new_a, new_a)
    return res


def part2(inp_: Input):
    return search(0, 0, inp_)


example1 = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1)) == "4,6,3,5,6,3,5,2,1,0"


def test_part1():
    res = part1(parse_input(read_input()))
    print(res)
    assert res == "5,1,4,0,5,1,0,2,6"


example2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


def test_part2_example():
    assert part2(parse_input(example2.splitlines())) == 117440


def test_part2():
    res = part2(parse_input(read_input()))
    print(res)
    assert res == 202322936867370
