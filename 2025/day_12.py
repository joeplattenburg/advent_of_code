import sys
import numpy as np


def parse_top(s: str) -> tuple[int, np.ndarray]:
    lines = s.split('\n')
    num = int(lines.pop(0).strip().replace(':', ''))
    return num, np.array([list(line) for line in lines])


def parse_bottom(s: str) -> tuple[tuple[int, int], list[int]]:
    left, right = s.split(':')
    x, y = left.split('x')
    return (int(x), int(y)), [int(r) for r in right.split()]


if __name__ == "__main__":
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        *top, bottom = f.read().split('\n\n')
    shapes = dict(parse_top(t) for t in top)
    regions = [parse_bottom(b) for b in bottom.split('\n')]
    part1 = sum(bool((x // 3) * (y // 3) >= sum(s)) for (x, y), s in regions)
    print('Part 1:', part1)
