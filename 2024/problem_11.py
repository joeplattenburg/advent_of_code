import sys


def stone_count_after_blinks(stone: int, n_blinks: int = 1, total: int = 0):
    if n_blinks == 0:
        return 1
    else:
        new_stones = blink(stone)
        for new_stone in new_stones:
            total += stone_count_after_blinks(new_stone, n_blinks - 1)
        return total


def blink(stone: int) -> list[int]:
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
    part1 = sum(stone_count_after_blinks(stone, n_blinks=25) for stone in stones)
    print(f'Part 1: {part1}')
    part2 = sum(stone_count_after_blinks(stone, n_blinks=75) for stone in stones)
    print(f'Part 2: {part2}')
