from __future__ import annotations

import dataclasses
import operator
import re
from typing import Callable

from black.trans import defaultdict


def read_input() -> list[str]:
    with open("../input/day24.txt") as f:
        return [l.strip() for l in f.readlines()]


@dataclasses.dataclass
class Node(object):
    nargs: int
    op: Callable[[list[int]], int]
    children: list[str] = dataclasses.field(default_factory=list)
    values: list[int] = dataclasses.field(default_factory=list)
    res: int | None = None

    def push(self, value: int, nodes: dict[str, Node]):
        self.values.append(value)

        if len(self.values) == self.nargs:
            self.res = self.op(*self.values)
            for c in self.children:
                nodes[c].push(self.res, nodes)


@dataclasses.dataclass
class Input(object):
    nodes: dict[str, Node]
    initial_values: dict[str, int]


def parse_input(lines: list[str]) -> Input:
    nodes: dict[str, Node] = {}
    initial_values: dict[str, int] = {}
    pass_though = lambda x: x

    for line in lines:
        if match := re.match("(\w+): (\d)", line):
            node_name = match.group(1)
            value = int(match.group(2))
            nodes[node_name] = Node(1, pass_though)
            initial_values[node_name] = value
        elif match := re.match("(\w+) (\w+) (\w+) -> (\w+)", line):
            _, op_name, _, out = match.groups()
            op_name = op_name.lower()
            try:
                op = getattr(operator, op_name)
            except AttributeError:
                op = getattr(operator, op_name + "_")
            nodes[out] = Node(2, op)

    for line in lines:
        if match := re.match("(\w+) (\w+) (\w+) -> (\w+)", line):
            inp1, _, inp2, out = match.groups()
            nodes[inp1].children.append(out)
            nodes[inp2].children.append(out)

    return Input(nodes, initial_values)


def part1(inp: Input) -> int:
    for inp_node, inp_value in inp.initial_values.items():
        inp.nodes[inp_node].push(inp_value, inp.nodes)

    zs = sorted((k for k in inp.nodes.keys() if k.startswith("z")), reverse=True)

    res = 0
    for z in zs:
        res = res * 2 + inp.nodes[z].res
    return res


def part2(lines: list[str]):

    def key(inp1, op_name, inp2):
        return tuple(sorted((inp1, op_name, inp2)))

    eq = {}
    for line in lines:
        if match := re.match("(\w+) (\w+) (\w+) -> (\w+)", line):
            inp1, op_name, inp2, out = match.groups()
            eq[key(inp1, op_name, inp2)] = out

    res = defaultdict(list)

    # Half-adder
    carry_in = eq[key("x00", "AND", "y00")]
    res[carry_in].append("c00")

    for b in range(1, 45):
        tmp_1 = eq[key(f"x{b:02}", "XOR", f"y{b:02}")]
        res[tmp_1].append(f"tmp{b:02}-1")

        try:
            zb = eq[key(tmp_1, "XOR", carry_in)]
            res[zb].append(f"z{b:02}")
            if not zb.startswith("z"):
                print(f"z{b:02} not found here", (tmp_1, "XOR", carry_in))
        except KeyError:
            print(f"z{b:02} is missing for", (tmp_1, "XOR", carry_in))

        tmp_2 = eq[key(f"y{b:02}", "AND", f"x{b:02}")]
        res[tmp_2].append(f"tmp{b:02}-2")

        try:
            tmp_3 = eq[key(carry_in, "AND", tmp_1)]
            res[tmp_3].append(f"tmp{b:02}-3")
        except KeyError:
            print(f"tmp{b:02}-3 is missing for", (carry_in, "AND", tmp_1))
            tmp_3 = "UNKNOWN"

        try:
            carry_out = eq[key(tmp_3, "OR", tmp_2)]
            res[carry_out].append(f"c{b:02}")
        except KeyError:
            print(f"c{b:02} is missing for", (tmp_3, "OR", tmp_2))
            carry_out = "UNKNOWN"

        carry_in = carry_out

    return res


example1 = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02""".splitlines()

example2 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj""".splitlines()


def test_part1_examples():
    assert part1(parse_input(example1)) == 4
    assert part1(parse_input(example2)) == 2024


def test_part1():
    res = part1(parse_input(read_input()))
    print(res)
    assert res == 36902370467952


def test_part2():
    res = part2(read_input())
    print(res)
    print(",".join(sorted(["z10", "mkk", "z14", "qbw", "cvp", "wjb", "z34", "wcb"])))
