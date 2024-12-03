import sys


if __name__ == "__main__":
    input_path = sys.argv[1]
    left, right = [], []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            l, r = line.strip().split()
            left.append(int(l))
            right.append(int(r))
    left = sorted(left)
    right = sorted(right)
    diffs = 0
    for l, r in zip(left, right):
        diffs += abs(l - r)
    print(f'Part 1: {diffs}')
