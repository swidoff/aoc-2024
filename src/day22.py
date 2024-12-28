def read_input() -> list[str]:
    with open("../input/day22.txt") as f:
        return [l.strip() for l in f.readlines()]


def parse_input(lines: list[str]) -> list[int]:
    return list(map(int, lines))


def evolve_1(secret):
    v1 = secret * 64
    secret ^= v1
    secret %= 16777216
    v2 = secret // 32
    secret ^= v2
    secret %= 16777216
    v3 = secret * 2048
    secret ^= v3
    secret %= 16777216
    return secret


def evolve_n(initial_secret: int, n: int) -> int:
    secret = initial_secret
    for _ in range(n):
        secret = evolve_1(secret)
        # print(secret)
    return secret


def part1(initial_secrets: list[int], n: int) -> int:
    return sum(map(lambda x: evolve_n(x, n), initial_secrets))


def changes_n(initial_secret: int, n: int) -> (list[int], list[int]):
    secret = initial_secret
    changes = []
    prices = []
    for i in range(n - 1):
        new_secret = evolve_1(secret)
        changes.append(new_secret % 10 - secret % 10)
        prices.append(new_secret % 10)
        secret = new_secret
    return changes, prices


def part2(initial_secrets: list[int]) -> int:
    res = {}
    for n in initial_secrets:
        changes, prices = changes_n(n, 2001)
        n_res = {}
        for i in range(3, len(changes) - 3):
            seq = tuple(changes[i : i + 4])
            if seq not in n_res:
                price = prices[i + 3]
                n_res[seq] = price
                res[seq] = res.get(seq, 0) + price
    return max(res.values())


example1 = """1
10
100
2024""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1), 2000) == 37327623


def test_part1():
    res = part1(parse_input(read_input()), 2000)
    print(res)
    assert res == 20401393616


example2 = """1
2
3
2024""".splitlines()


def test_part2_example():
    assert changes_n(123, 10) == (
        [-3, 6, -1, -1, 0, 2, -2, 0, -2],
        [0, 6, 5, 4, 4, 6, 4, 4, 2],
    )

    assert part2(parse_input(example2)) == 23


def test_part2():
    res = part2(parse_input(read_input()))
    print(res)
    assert res == 2272
    # 2268 is too low
