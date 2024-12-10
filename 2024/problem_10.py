import sys
import numpy as np


def get_score(grid: np.array, start: tuple[int, int], ends: set = None) -> set:
    ends = ends or set()
    for neighbor in get_neighbors(grid, *start):
        if grid[*neighbor] == grid[*start] + 1:
            if grid[*neighbor] == 9:
                ends.add(neighbor)
            else:
                ends |= get_score(grid, neighbor, ends)
    return ends


def get_rating(grid: np.array, start: tuple[int, int]) -> int:
    n_trails = 0
    for neighbor in get_neighbors(grid, *start):
        if grid[*neighbor] == grid[*start] + 1:
            if grid[*neighbor] == 9:
                n_trails += 1
            else:
                n_trails += get_rating(grid, neighbor)
    return n_trails


def get_neighbors(grid: np.array, i: int, j: int) -> list[tuple[int, int]]:
    return [
        (i + di, j + dj)
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if (0 <= i + di < grid.shape[0]) and (0 <= j + dj < grid.shape[1])
    ]


if __name__ == "__main__":
    input_path = sys.argv[1]
    grid = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            grid.append([-1 if val == '.' else int(val) for val in line.strip()])
    grid = np.array(grid)
    trailheads = zip(*np.where(grid == 0))
    part1, part2 = 0, 0
    for trailhead in trailheads:
        part1 += len(get_score(grid, trailhead))
        part2 += get_rating(grid, trailhead)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
