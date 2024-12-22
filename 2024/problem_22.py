import sys
from collections import defaultdict


def parse_input(input_path) -> list[int]:
    with open(input_path, 'r') as f:
        out = [int(line.strip()) for line in f.readlines()]
    return out


def next_number(n: int) -> int:
    n = ((n * (2 ** 6)) ^ n) % (2 ** 24)
    n = ((n // (2 ** 5)) ^ n) % (2 ** 24)
    n = ((n * (2 ** 11)) ^ n) % (2 ** 24)
    return n


def cycle_diffs(d: list[int], new: int):
    d.append(new)
    if len(d) > 4:
        d.pop(0)


if __name__ == "__main__":
    input_path = sys.argv[1]
    secrets = parse_input(input_path)
    n_rounds = 2000
    part1 = 0
    counter = defaultdict(int)
    for secret in secrets:
        price = int(str(secret)[-1])
        already_seen = set()
        diffs = []
        for i in range(n_rounds):
            secret = next_number(secret)
            new_price = int(str(secret)[-1])
            cycle_diffs(diffs, new_price - price)
            if len(diffs) == 4:
                seq = tuple(diffs)
                if seq not in already_seen:
                    already_seen.add(seq)
                    counter[seq] += new_price
            price = new_price
        part1 += secret
    part2 = max(counter.values())
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
