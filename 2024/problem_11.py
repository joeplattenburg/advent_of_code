import sys
from functools import cache


@cache
def blink(stone: int, n_times: int = 1) -> int:
    if n_times == 0:
        return 1
    else:
        return sum(blink(new_stone, n_times - 1) for new_stone in _blink(stone))


def _blink(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(stone_str := str(stone)) % 2 == 0:
        mid = len(stone_str) // 2
        return [int(stone_str[:mid]), int(stone_str[mid:])]
    else:
        return [2024 * stone]


if __name__ == "__main__":
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        stones = [int(c) for c in f.read().strip().split()]
    part1 = sum(blink(stone, n_times=25) for stone in stones)
    print(f'Part 1: {part1}')
    part2 = sum(blink(stone, n_times=75) for stone in stones)
    print(f'Part 2: {part2}')
