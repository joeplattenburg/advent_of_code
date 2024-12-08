import sys
from collections import defaultdict

Location = tuple[int, int]


def parse_input(input_path: str) -> tuple[dict[str, list[Location]], tuple[int, int]]:
    antennas = defaultdict(list)
    with open(input_path, 'r') as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line.strip()):
                if c != '.':
                    antennas[c] += [(i, j)]
    return antennas, (i + 1, j + 1)


def find_antinodes(antennas: list[Location], grid_shape: tuple[int, int], allow_harmonics: bool = False) -> set[Location]:
    out = set()
    for i, a1 in enumerate(antennas):
        for a2 in antennas[:i]:
            for an in antinodes_from_pair(a1, a2, grid_shape, allow_harmonics):
                out.add(an)
    return out


def antinodes_from_pair(
        a1: Location, a2: Location, grid_shape: tuple[int, int], allow_harmonics: bool
) -> list[Location]:
    out = []
    dy, dx = a2[0] - a1[0], a2[1] - a1[1]
    if allow_harmonics:
        n = 0
        while True:
            test_loc = a2[0] + n * dy, a2[1] + n * dx
            if on_grid(test_loc, grid_shape):
                out.append(test_loc)
            else:
                break
            n += 1
        n = 0
        while True:
            test_loc = a1[0] - n * dy, a1[1] - n * dx
            if on_grid(test_loc, grid_shape):
                out.append(test_loc)
            else:
                break
            n += 1
    else:
        test_loc = (a2[0] + dy, a2[1] + dx)
        if on_grid(test_loc, grid_shape):
            out.append(test_loc)
        test_loc = (a1[0] - dy, a1[1] - dx)
        if on_grid(test_loc, grid_shape):
            out.append(test_loc)
    return out


def on_grid(loc: Location, grid_shape: tuple[int, int]) -> bool:
    return (0 <= loc[0] < grid_shape[0]) and (0 <= loc[1] < grid_shape[1])


if __name__ == "__main__":
    input_path = sys.argv[1]
    antenna_groups, grid_shape = parse_input(input_path)
    part1, part2 = set(), set()
    for frequency, antennas in antenna_groups.items():
        part1 |= find_antinodes(antennas, grid_shape)
        part2 |= find_antinodes(antennas, grid_shape, allow_harmonics=True)
    print(f'Part 1: {len(part1)}')
    print(f'Part 2: {len(part2)}')
