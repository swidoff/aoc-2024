import dataclasses
import itertools
from collections import defaultdict


def read_input() -> str:
    with open("../input/day09.txt") as f:
        return f.readline().strip()


def part1(inp_: str) -> int:
    disk = []
    for file_id, i in enumerate(range(0, len(inp_), 2)):
        for _ in range(int(inp_[i])):
            disk.append(file_id)

        if i + 1 < len(inp_):
            for _ in range(int(inp_[i + 1])):
                disk.append(".")

    head = 0
    tail = len(disk) - 1
    while head < tail:
        if disk[head] == ".":
            disk[head] = disk[tail]
            tail -= 1
            while disk[tail] == ".":
                tail -= 1
        head += 1

    return sum(i * j for i, j in enumerate(disk[: tail + 1]))


@dataclasses.dataclass(frozen=True)
class Blocks(object):
    file_id: int | None
    n: int
    free: bool


def part2(inp_: str) -> int:
    disk = []
    file_id = 0
    for i, n in enumerate(inp_):
        if i % 2 == 0:
            disk.append(Blocks(file_id, int(n), free=False))
            file_id += 1
        else:
            disk.append(Blocks(None, int(n), free=True))

    for file_id_ in range(file_id - 1, -1, -1):
        file_idx = 0
        for i, blocks in enumerate(reversed(disk)):
            if not blocks.free and file_id_ == blocks.file_id:
                file_idx = len(disk) - i - 1
                break

        new_disk = []
        file_blocks = disk[file_idx]
        for i in range(file_idx):
            blocks = disk[i]
            if blocks.free and blocks.n >= file_blocks.n:
                new_disk.append(file_blocks)
                if blocks.n > file_blocks.n:
                    new_disk.append(Blocks(None, blocks.n - file_blocks.n, free=True))
                new_disk.extend(disk[i + 1 : file_idx])
                new_disk.append(Blocks(None, file_blocks.n, free=True))
                new_disk.extend(disk[file_idx + 1 :])
                disk = new_disk
                break
            else:
                new_disk.append(blocks)

    i = 0
    res = 0
    for blocks in disk:
        if not blocks.free:
            for _ in range(blocks.n):
                res += blocks.file_id * i
                i += 1
        else:
            i += blocks.n

    return res


example1 = "2333133121414131402"


def test_part1_example():
    assert part1(example1) == 1928


def test_part1():
    res = part1(read_input())
    print(res)
    assert res == 6398608069280


def test_part2_example():
    assert part2(example1) == 2858


def test_part2():
    res = part2(read_input())
    print(res)
    assert res == 6427437134372
