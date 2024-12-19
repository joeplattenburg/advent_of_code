import sys
from functools import cache


def parse_input(input_path: str) -> tuple[list[str], list[str]]:
    with open(input_path, 'r') as f:
        towels, patterns = f.read().split('\n\n')
    return [t.strip() for t in towels.split(',')], [p.strip() for p in patterns.split('\n')]


@cache
def valid_pattern(pattern: str) -> bool:
    any_match = False
    for towel in towels:
        if pattern.startswith(towel):
            if not (remainder := pattern[len(towel):]):
                return True
            else:
                if valid_pattern(remainder):
                    any_match = True
    return any_match


if __name__ == "__main__":
    input_path = sys.argv[1]
    towels, patterns = parse_input(input_path)
    part1 = []
    for i, pattern in enumerate(patterns):
        if valid_pattern(pattern):
            part1.append(pattern)
    part2 = 0
    print(f'Part 1: {len(part1)}')
    print(f'Part 2: {part2}')
