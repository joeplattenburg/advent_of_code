import sys
from collections import defaultdict

if __name__ == "__main__":
    input_path = sys.argv[1]
    left, right = [], []
    right_d = defaultdict(int)
    with open(input_path, 'r') as f:
        for line in f.readlines():
            l, r = line.strip().split()
            left.append(int(l))
            right.append(int(r))
            right_d[int(r)] += 1
    left = sorted(left)
    right = sorted(right)
    diffs = 0
    similarity_score = 0
    for l, r in zip(left, right):
        diffs += abs(l - r)
        similarity_score += l * right_d.get(l, 0)
    print(f'Part 1: {diffs}')
    print(f'Part 2: {similarity_score}')
