import itertools

from collections import defaultdict


def read_input() -> list[str]:
    with open("../input/day23.txt") as f:
        return [l.strip() for l in f.readlines()]


def parse_input(lines: list[str]) -> set[tuple[str, str]]:
    res = set()
    for line in lines:
        cmp1, cmp2 = line.split("-", maxsplit=1)
        start = min(cmp1, cmp2)
        end = max(cmp1, cmp2)
        res.add((start, end))
    return res


def part1(inp: set[tuple[str, str]]) -> int:
    res = set()
    computers = {c1 for c1, _ in inp} | {c2 for _, c2 in inp}
    for cmp1, cmp2 in inp:
        for cmp3 in computers:
            if cmp3 == cmp1 or cmp3 == cmp2:
                continue

            if not (
                cmp1.startswith("t") or cmp2.startswith("t") or cmp3.startswith("t")
            ):
                continue

            if (min(cmp1, cmp3), max(cmp1, cmp3)) in inp and (
                min(cmp2, cmp3),
                max(cmp2, cmp3),
            ) in inp:
                res.add(tuple(sorted((cmp1, cmp2, cmp3))))

    return len(res)


def part2(inp: set[tuple[str, str]]) -> str:
    d = defaultdict(list)
    for c1, c2 in inp:
        d[c1].append(c2)
        d[c2].append(c1)

    res = None
    for c, others in d.items():
        for comb in itertools.product([True, False], repeat=len(others)):
            subset = [o for o, inc in zip(others, comb) if inc]
            if all(
                o1 == o2 or (min(o1, o2), max(o1, o2)) in inp
                for o1 in subset
                for o2 in subset
            ) and (res is None or len(res) < len(subset) + 1):
                subset.append(c)
                res = sorted(subset)

    return ",".join(res)


example1 = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1)) == 7


def test_part1():
    assert part1(parse_input(read_input())) == 1184


def test_part2_example():
    assert part2(parse_input(example1)) == "co,de,ka,ta"


def test_part2():
    res = part2(parse_input(read_input()))
    print(res)
    assert res == "hf,hz,lb,lm,ls,my,ps,qu,ra,uc,vi,xz,yv"
