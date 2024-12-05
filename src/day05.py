from collections import defaultdict
from dataclasses import dataclass


def read_input() -> list[str]:
    with open("../input/day05.txt") as f:
        return [s.strip() for s in f.readlines()]


@dataclass(frozen=True)
class Input(object):
    dag: dict[int, set[int]]
    updates: list[list[int]]


def parse_input(lines: list[str]) -> Input:
    rules = defaultdict(set)
    update_start = 0
    for i, line in enumerate(lines):
        if line == "":
            update_start = i + 1
            break
        n1, n2 = line.split("|", maxsplit=1)
        rules[int(n1)].add(int(n2))

    updates = [[int(n) for n in line.split(",")] for line in lines[update_start:]]
    return Input(rules, updates)


def is_sorted(indexes: dict[int, list[int]], dag: dict[int, set[int]]) -> bool:
    for before in indexes:
        for after in dag[before]:
            if after in indexes and indexes[before] > indexes[after]:
                return False
    return True


def part1(inp_: Input) -> int:
    dag = inp_.dag
    updates = inp_.updates

    res = 0
    for update in updates:
        indexes = {n: i for i, n in enumerate(update)}
        if is_sorted(indexes, dag):
            res += update[len(update) // 2]

    return res


def topo_sort(nodes: list[int], dag: dict[int, set[int]]) -> list[int]:
    small_dag = {}
    node_set = set(nodes)
    for n in nodes:
        small_dag[n] = dag[n] & node_set

    """
    L ← Empty list that will contain the sorted elements
    S ← Set of all nodes with no incoming edge
    
    while S is not empty do
        remove a node n from S
        add n to L
        for each node m with an edge e from n to m do
            remove edge e from the graph
            if m has no other incoming edges then
                insert m into S
    
    if graph has edges then
        return error   (graph has at least one cycle)
    else 
        return L   (a topologically sorted order)
    """
    l = []
    s = {n for n in nodes if no_incoming_edges(n, small_dag)}
    while s:
        n = s.pop()
        l.append(n)
        for m in list(small_dag[n]):
            small_dag[n].remove(m)
            if no_incoming_edges(m, small_dag):
                s.add(m)

    return l


def no_incoming_edges(n, dag):
    return all(n not in deps for deps in dag.values())


def part2(inp_: Input) -> int:
    dag = inp_.dag
    updates = inp_.updates

    res = 0
    for update in updates:
        indexes = {n: i for i, n in enumerate(update)}
        if not is_sorted(indexes, dag):
            new_update = topo_sort(update, dag)
            res += new_update[len(new_update) // 2]

    return res


example1 = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""".splitlines()


def test_part1_example():
    assert part1(parse_input(example1)) == 143


def test_part1():
    # print(part1(parse_input(read_input())))
    assert part1(parse_input(read_input())) == 5208


def test_part2_example():
    assert part2(parse_input(example1)) == 123


def test_part2():
    assert part2(parse_input(read_input())) == 6732
