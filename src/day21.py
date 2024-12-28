from collections import deque
from functools import cache


def read_input() -> list[str]:
    with open("../input/day21.txt") as f:
        return [l.strip() for l in f.readlines()]


NUMERIC_KEYPAD = {
    "7": [("8", ">"), ("4", "v")],
    "8": [("9", ">"), ("5", "v"), ("7", "<")],
    "9": [("6", "v"), ("8", "<")],
    "4": [("7", "^"), ("5", ">"), ("1", "v")],
    "5": [("8", "^"), ("6", ">"), ("2", "v"), ("4", "<")],
    "6": [("9", "^"), ("3", "v"), ("5", "<")],
    "1": [("4", "^"), ("2", ">")],
    "2": [("5", "^"), ("1", "<"), ("3", ">"), ("0", "v")],
    "3": [("6", "^"), ("2", "<"), ("A", "v")],
    "0": [("2", "^"), ("A", ">")],
    "A": [("3", "^"), ("0", "<")],
}

DIR_KEYPAD = {
    "^": {"A": [">"], "v": ["v"], "<": ["v<"], ">": ["v>", ">v"]},
    "A": {"^": ["<", "v<^"], ">": ["v", "<v>"], "v": ["v<", "<v"], "<": ["v<<", "<v<"]},
    "<": {"v": [">"], "^": [">^", ">>^<"], ">": [">>", ">^>v"], "A": [">>^", ">^>"]},
    "v": {"<": ["<"], "^": ["^"], ">": [">"], "A": ["^>", ">^"]},
    ">": {"v": ["<", "^<v"], "A": ["^", "<^>"], "^": ["^<", "<^"], "<": ["<<", "^<v<"]},
}


@cache
def number_pad_paths(start: str, end: str) -> set[str]:
    q = deque()
    q.append((start, "", set()))
    res = set()
    while q:
        num, keys, seen = q.popleft()
        if num == end:
            res.add(keys)
            continue

        for next_num, key in NUMERIC_KEYPAD[num]:
            if next_num not in seen:
                q.append((next_num, keys + key, seen | {next_num}))

    return res


@cache
def shortest_path(keys: str, level: int, max_levels: int) -> int:
    if level == 0:
        res = 0
        for key1, key2 in zip("A" + keys, keys):
            res += min(
                shortest_path(path + "A", level + 1, max_levels)
                for path in number_pad_paths(key1, key2)
            )
        return res
    elif level < max_levels:
        res = 0
        new_keys = "A" + keys
        for key1, key2 in zip(new_keys, new_keys[1:]):
            res += min(
                shortest_path(path + "A", level + 1, max_levels)
                for path in DIR_KEYPAD[key1].get(key2, [""])
            )
        return res
    else:
        return len(keys)


def part1(lines: list[str]) -> int:
    return sum(shortest_path(line, 0, 3) * int(line[:3]) for line in lines)


def part2(lines: list[str]) -> int:
    return sum(shortest_path(line, 0, 26) * int(line[:3]) for line in lines)


def test_shortest_path():
    assert shortest_path("029A", 0, 3) == 68
    assert shortest_path("980A", 0, 3) == 60
    assert shortest_path("179A", 0, 3) == 68
    assert shortest_path("456A", 0, 3) == 64
    assert shortest_path("379A", 0, 3) == 64


example1 = """029A
980A
179A
456A
379A
""".splitlines()


def test_part1_example():
    assert part1(example1) == 126384


def test_part1():
    res = part1(read_input())
    print(res)


def test_part2():
    res = part2(read_input())
    print(res)
    assert res == 223285811665866
