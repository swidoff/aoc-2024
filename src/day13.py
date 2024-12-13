import dataclasses
import re


def read_input() -> list[str]:
    with open("../input/day13.txt") as f:
        return [l.strip() for l in f.readlines()]


@dataclasses.dataclass(frozen=True)
class Input(object):
    xa: int
    xb: int
    ya: int
    yb: int
    x: int
    y: int


# XA*a + XB*b = X
# YA*a + YB*b = Y

# b = (X - XA*a)/XB
# YA*a + YB*(X/XB - XA*a/XB) = Y
# YA*a + YB*X/XB - YB*XA*a/XB = Y
# YA*a - YB*XA*a/XB = y - YB*X/XB
# XB*YA*a/XB - YB*XA*a/XB = Y - YB*X/XB
# (((XB*YA) - (YB*XA))/XB)*a = Y - YB*X/XB
# a = (Y - (YB*X/XB)) / (((XB*YA) - (YB*XA))/XB)

# a = (Y - (YB*X/XB)) / (((XB*YA) - (YB*XA))/XB)
# b = (X - XA*a)/XB


def parse_input(lines: list[str]) -> list[Input]:
    res = []
    for i in range(0, len(lines), 4):
        line1, line2, line3 = lines[i : i + 3]
        xa, ya = re.match(r"Button A: X\+(\d+), Y\+(\d+)", line1).groups()
        xb, yb = re.match(r"Button B: X\+(\d+), Y\+(\d+)", line2).groups()
        x, y = re.match(r"Prize: X=(\d+), Y=(\d+)", line3).groups()
        res.append(Input(int(xa), int(xb), int(ya), int(yb), int(x), int(y)))
    return res


def part1(inp: list[Input]):
    res = 0
    for i in inp:
        xa, xb, ya, yb, x, y = dataclasses.astuple(i)
        a = (y - (yb * x / xb)) / (((xb * ya) - (yb * xa)) / xb)
        b = (x - xa * a) / xb
        if abs(a - round(a)) < 1e-4 and abs(b - round(b)) < 1e-4:
            res += a * 3 + b
    return res


def part2(inp: list[Input]):
    res = 0
    for i in inp:
        xa, xb, ya, yb, x, y = dataclasses.astuple(i)
        x += 10000000000000
        y += 10000000000000

        a = (y - (yb * x / xb)) / (((xb * ya) - (yb * xa)) / xb)
        b = (x - xa * a) / xb
        if abs(a - round(a)) < 1e-4 and abs(b - round(b)) < 1e-4:
            res += a * 3 + b
    return res


example1 = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1)) == 480


def test_part1():
    res = part1(parse_input(read_input()))
    print(res)
    assert res == 35729.0


def test_part2():
    res = part2(parse_input(read_input()))
    print(res)
    assert res == 88584689879723
