import sys


def get_joltage(s: str, n: int) -> int:
    max_vals = []
    remainder = s
    for i in range(n, 0, -1):
        max_val = max(remainder[:-(i - 1)] if i > 1 else remainder)
        max_vals.append(max_val)
        max_ind = remainder.index(max_val)
        remainder = remainder[(max_ind + 1):]
    return int(''.join(max_vals))


if __name__ == "__main__":
    input_path = sys.argv[1]
    part1 = 0
    part2 = 0
    with open(input_path, 'r') as f:
        for line in f.readlines():
            part1 += get_joltage(line.strip(), n=2)
            part2 += get_joltage(line.strip(), n=12)
    print('Part 1:', part1)
    print('Part 2:', part2)
