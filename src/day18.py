def read_input() -> list[str]:
    with open("../input/day18.txt") as f:
        return [l.strip() for l in f.readlines()]


def parse_input(lines: list[str]) -> list[(int, int)]:
    res = []
    for line in lines:
        v1, v2 = line.split(",")
        res.append((int(v1), int(v2)))
    return res


def path_to_exit(
    bytes_: list[(int, int)], n: int, dim: int, first: bool = False
) -> int:
    blocked = set(bytes_[:n])
    seen = {}
    q = [(0, 0, 0)]
    max_dist = dim**2
    while q:
        r, c, d = q.pop()
        if seen.get((r, c), max_dist) <= d:
            continue

        seen[(r, c)] = d

        if (r, c) == (dim - 1, dim - 1):
            if first:
                break
            continue

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < dim and 0 <= nc < dim and (nr, nc) not in blocked:
                q.append((nr, nc, d + 1))

    return seen.get((dim - 1, dim - 1), -1)


def part2(bytes_: list[(int, int)], dim: int):
    lo = 0
    hi = len(bytes_)
    while lo < hi:
        mid = (lo + hi) // 2
        if path_to_exit(bytes_, mid, dim, True) == -1:
            hi = mid
        else:
            lo = mid + 1
    r, c = bytes_[lo - 1]
    return f"{r},{c}"


example1 = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def test_part1_example():
    assert path_to_exit(parse_input(example1.splitlines()), 12, 7) == 22


def test_part1():
    res = path_to_exit(parse_input(read_input()), 1024, 71)
    print(res)
    assert res == 324


def test_part2_example():
    assert part2(parse_input(example1.splitlines()), 7) == "6,1"


def test_part2():
    res = part2(parse_input(read_input()), 71)
    print(res)
    assert res == "46,23"
