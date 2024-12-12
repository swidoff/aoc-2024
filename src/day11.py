import dataclasses
from functools import cache


def read_input() -> str:
    with open("../input/day11.txt") as f:
        return f.readline().strip()


def parse_input(line: str) -> list[str]:
    return line.split(" ")


@cache
def blink_stones(stone: str, blinks: int) -> int:
    if blinks == 0:
        return 1

    if stone == "0":
        res = blink_stones("1", blinks - 1)
    elif len(stone) % 2 == 0:
        new_stone1 = str(int(stone[: len(stone) // 2]))
        new_stone2 = str(int(stone[len(stone) // 2 :]))
        res = blink_stones(new_stone1, blinks - 1) + blink_stones(
            new_stone2, blinks - 1
        )
    else:
        res = blink_stones(str(int(stone) * 2024), blinks - 1)

    return res


def part1(inp: list[str]) -> int:
    return sum(blink_stones(s, 25) for s in inp)


def part2(inp: list[str]) -> int:
    return sum(blink_stones(s, 75) for s in inp)


example1 = "125 17"


def test_part1_example():
    assert part1(parse_input(example1)) == 55312


def test_part1():
    assert part1(parse_input(read_input())) == 183620


def test_part2():
    res = part2(parse_input(read_input()))
    print(res)
    assert res == 220377651399268
