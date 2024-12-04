def read_input() -> list[str]:
    with open("../input/day04.txt") as f:
        return f.readlines()


def part1(lines: list[str]) -> int:
    n_rows = len(lines)
    n_cols = len(lines[0])

    offsets = [
        [(0, 0), (0, 1), (0, 2), (0, 3)],  # Right
        [(0, 0), (0, -1), (0, -2), (0, -3)],  # Left
        [(0, 0), (1, 0), (2, 0), (3, 0)],  # Down
        [(0, 0), (-1, 0), (-2, 0), (-3, 0)],  # Up
        [(0, 0), (1, 1), (2, 2), (3, 3)],  # Right Down
        [(0, 0), (-1, 1), (-2, 2), (-3, 3)],  # Right Up
        [(0, 0), (1, -1), (2, -2), (3, -3)],  # Left Down
        [(0, 0), (-1, -1), (-2, -2), (-3, -3)],  # Left Up
    ]

    def is_xmas(r: int, c: int, offsets: list[tuple[int, int]]) -> bool:
        return (
            all(0 <= r + ro < n_rows and 0 <= c + co < n_cols for (ro, co) in offsets)
            and "".join(lines[r + ro][c + co] for ro, co in offsets) == "XMAS"
        )

    res = 0
    for r in range(n_rows):
        for c in range(n_cols):
            res += sum(is_xmas(r, c, o) for o in offsets)
    return res


xmas_words = {"MSAMS", "MMASS", "SSAMM", "SMASM"}


def part2(lines: list[str]) -> int:
    n_rows = len(lines)
    n_cols = len(lines[0])
    offsets = [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)]

    res = 0
    for r in range(1, n_rows - 1):
        for c in range(1, n_cols - 1):
            res += "".join(lines[r + ro][c + co] for ro, co in offsets) in xmas_words
    return res


example1 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".splitlines()


def test_part1_example():
    assert part1(example1) == 18


def test_part1():
    # print(part1(read_input()))
    assert part1(read_input()) == 2642


def test_part2_example():
    assert part2(example1) == 9


def test_part2():
    # print(part2(read_input()))
    assert part2(read_input()) == 1974
