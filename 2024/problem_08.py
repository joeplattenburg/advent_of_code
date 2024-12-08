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


def find_antinodes(antennas: list[Location], grid_shape: tuple[int, int]) -> set[Location]:
    out = set()
    for i, a1 in enumerate(antennas):
        for a2 in antennas[:i]:
            for an in antinodes_from_pair(a1, a2):
                if on_grid(an, grid_shape):
                    out.add(an)
    return out


def on_grid(loc: Location, grid_shape: tuple[int, int]) -> bool:
    return (0 <= loc[0] < grid_shape[0]) and (0 <= loc[1] < grid_shape[1])


def antinodes_from_pair(a1: Location, a2: Location) -> tuple[Location, Location]:
    dy, dx = a2[0] - a1[0], a2[1] - a1[1]
    return (a2[0] + dy, a2[1] + dx), (a1[0] - dy, a1[1] - dx)


if __name__ == "__main__":
    input_path = sys.argv[1]
    part2 = 0
    antenna_groups, grid_shape = parse_input(input_path)
    antinodes = set()
    for frequency, antennas in antenna_groups.items():
        antinodes |= find_antinodes(antennas, grid_shape)
    print(f'Part 1: {len(antinodes)}')
    print(f'Part 2: {part2}')
