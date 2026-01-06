import sys


def parse(s: str) -> list[tuple[int, int]]:
    out = []
    for r in s.split(','):
        a, b = r.split('-')
        out.append((int(a), int(b)))
    return out


def is_invalid(num: int, part2: bool) -> bool:
    num_str = str(num)
    n = len(num_str)
    if n < 2:
        return False
    check_lens = range(1, n) if part2 else [n // 2]
    for i in check_lens:
        if n % i == 0:
            if num_str == (num_str[:i] * n)[:n]:
                return True
    else:
        return False


if __name__ == "__main__":
    input_path = sys.argv[1]
    part1 = 0
    part2 = 0
    with open(input_path, 'r') as f:
        ranges = parse(f.read().strip())
    for a, b in ranges:
        for i in range(a, b + 1):
            if is_invalid(i, part2=False):
                part1 += i
            if is_invalid(i, part2=True):
                part2 += i
    print('Part 1:', part1)
    print('Part 2:', part2)
