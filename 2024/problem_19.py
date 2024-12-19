import sys
from functools import cache


def parse_input(input_path: str) -> tuple[list[str], list[str]]:
    with open(input_path, 'r') as f:
        towels, patterns = f.read().split('\n\n')
    return [t.strip() for t in towels.split(',')], [p.strip() for p in patterns.split('\n')]


@cache
def valid_pattern_count(pattern: str) -> int:
    match_count = 0
    for towel in towels:
        if pattern.startswith(towel):
            if not (remainder := pattern[len(towel):]):
                match_count += 1
            else:
                match_count += valid_pattern_count(remainder)
    return match_count


if __name__ == "__main__":
    input_path = sys.argv[1]
    towels, patterns = parse_input(input_path)
    counts = [valid_pattern_count(p) for p in patterns]
    counts = [c for c in counts if c > 0]
    print(f'Part 1: {len(counts)}')
    print(f'Part 2: {sum(counts)}')
