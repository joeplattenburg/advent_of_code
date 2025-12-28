import sys
from itertools import combinations


coord = tuple[int, int]

def parse_line(s: str) -> tuple[int, ...]:
    return tuple([int(i) for i in s.split(',')])


def size(a: coord, b: coord) -> int:
    return (abs(b[0] - a[0]) + 1) * (abs(b[1] - a[1]) + 1)


def intersect(a: coord, b: coord, coords: list[coord]) -> bool:
    xs = sorted((a[0], b[0]))
    ys = sorted((a[1], b[1]))
    for i, j in zip(coords, [*coords[1:], coords[0]]):
        direc = 'h' if i[1] == j[1] else 'v'
        if (
            (direc == 'h') and (ys[0] < i[1] < ys[1])
            and not ((i[0] <= xs[0] and j[0] <= xs[0]) or (i[0] >= xs[1] and j[0] >= xs[1]))
        ):
            return True
        if (
            (direc == 'v') and (xs[0] < i[0] < xs[1])
            and not ((i[1] <= ys[0] and j[1] <= ys[0]) or (i[1] >= ys[1] and j[1] >= ys[1]))
        ):
            return True
    return False


if __name__ == "__main__":
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        coords = [parse_line(line.strip()) for line in f.readlines()]
    part1 = max(size(a, b) for a, b in combinations(coords, 2))
    part2 = max(size(a, b) for a, b in combinations(coords, 2) if not intersect(a, b, coords))
    print('Part 1:', part1)
    print('Part 2:', part2)
