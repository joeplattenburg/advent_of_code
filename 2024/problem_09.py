import sys
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class Block:
    id: int
    start: int
    end: int


def parse_input(line: str) -> list[Block]:
    out = []
    pos = 0
    for i, c in enumerate(line):
        pos_new = pos + int(c)
        if i % 2 == 0:
            out.append(Block(id=i // 2, start=pos, end=pos_new))
        pos = pos_new
    return out


def push_block(new_block: Block, blocks: list[Block], loc: int) -> int:
    new_len = new_block.end - new_block.start
    new_start = blocks[loc - 1].end
    if loc >= len(blocks):
        blocks.insert(loc, Block(id=new_block.id, start=new_start, end=new_start + new_len))
        return loc + 1
    next_start = blocks[loc].start
    space_at_loc = next_start - new_start
    if space_at_loc >= new_len:
        blocks.insert(loc, Block(id=new_block.id, start=new_start, end=new_start + new_len))
        return loc + 1
    if space_at_loc == new_len:
        blocks.insert(loc, Block(id=new_block.id, start=new_start, end=new_start + new_len))
        return loc + 2
    else:
        blocks.insert(loc, Block(id=new_block.id, start=new_start, end=next_start))
        remainer = Block(id=new_block.id, start=next_start, end=next_start + new_len - space_at_loc)
        return push_block(remainer, blocks, loc=loc + 2)


def find_first_gap(blocks: list[Block], size: int) -> int | None:
    for i, (left, right) in enumerate(zip(blocks[:-1], blocks[1:])):
        gap = right.start - left.end
        if gap >= size:
            return i + 1
    return None


def get_index(blocks: list[Block], id: int) -> int | None:
    for i, block in enumerate(blocks):
        if block.id == id:
            return i


def checksum(blocks: list[Block]) -> int:
    return sum(sum(block.id * loc for loc in range(block.start, block.end)) for block in blocks)


if __name__ == "__main__":
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        memory_blocks = parse_input(f.read().strip())
    memory_blocks_1 = deepcopy(memory_blocks)
    pos = 1
    while pos < len(memory_blocks_1):
        end_block = memory_blocks_1.pop(-1)
        pos = push_block(end_block, memory_blocks_1, pos)
    part1 = checksum(memory_blocks_1)
    memory_blocks_2 = deepcopy(memory_blocks)
    for test_block in memory_blocks[-1::-1]:
        first_gap = find_first_gap(memory_blocks_2, size=(test_block.end - test_block.start))
        if first_gap is not None and memory_blocks_2[first_gap - 1].end < test_block.start:
            memory_blocks_2.pop(get_index(memory_blocks_2, test_block.id))
            push_block(test_block, memory_blocks_2, first_gap)
    part2 = checksum(memory_blocks_2)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
