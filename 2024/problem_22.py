import sys


def parse_input(input_path) -> list[int]:
    with open(input_path, 'r') as f:
        out = [int(line.strip()) for line in f.readlines()]
    return out


def next_number(n: int) -> int:
    n = ((n * (2 ** 6)) ^ n) % (2 ** 24)
    n = ((n // (2 ** 5)) ^ n) % (2 ** 24)
    n = ((n * (2 ** 11)) ^ n) % (2 ** 24)
    return n


if __name__ == "__main__":
    input_path = sys.argv[1]
    secrets = parse_input(input_path)
    part1 = 0
    for i, secret in enumerate(secrets):
        for _ in range(2000):
            secret = next_number(secret)
        print(f'Final value: {secret}')
        part1 += secret
    part2 = 0
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
