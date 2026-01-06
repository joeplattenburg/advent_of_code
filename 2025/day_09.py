import sys
from itertools import combinations


coord = tuple[int, int]


def parse_line(s: str) -> tuple[int, ...]:
    return tuple([int(i) for i in s.split(',')])


def size(a: coord, b: coord) -> int:
    return (abs(b[0] - a[0]) + 1) * (abs(b[1] - a[1]) + 1)


def intersect(square: tuple[coord, coord], segment: tuple[coord, coord]):
    i = 0 if segment[0][1] == segment[1][1] else 1
    return (
        (square[0][1 - i] < segment[0][1 - i] < square[1][1 - i])
        and not (
            (segment[0][i] <= square[0][i] and segment[1][i] <= square[0][i]) or
            (segment[0][i] >= square[1][i] and segment[1][i] >= square[1][i])
        )
    )


def any_intersect(a: coord, b: coord, segments: list[tuple[coord, coord]]) -> bool:
    square = (min(a[0], b[0]), min(a[1], b[1])), (max(a[0], b[0]), max(a[1], b[1]))
    for segment in segments:
        if intersect(square, segment):
            return True
    return False


if __name__ == "__main__":
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        coords = [parse_line(line.strip()) for line in f.readlines()]
    segments = list(zip(coords, [*coords[1:], coords[0]]))
    part1 = max(size(a, b) for a, b in combinations(coords, 2))
    part2 = max(size(a, b) for a, b in combinations(coords, 2) if not any_intersect(a, b, segments))
    print('Part 1:', part1)
    print('Part 2:', part2)
