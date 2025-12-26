import sys
import numpy as np


def count_neighbors(grid: np.ndarray, i: int, j: int) -> int:
    m, n = grid.shape
    return sum(
        grid[i + ii, j + jj] == '@'
        for ii in [-1, 0, 1]
        for jj in [-1, 0, 1]
        if (not ii == jj == 0)
        and (0 <= i + ii < m)
        and (0 <= j + jj < n)
    )


if __name__ == "__main__":
    input_path = sys.argv[1]
    part1 = 0
    part2 = 0
    grid = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            grid.append([c for c in line.strip()])
    grid = np.array(grid)
    for i, j in zip(*np.where(grid == '@')):
        part1 += int(count_neighbors(grid, i, j) < 4)

    stop = False
    while not stop:
        accessible_locs = []
        for i, j in zip(*np.where(grid == '@')):
            if count_neighbors(grid, i, j) < 4:
                accessible_locs.append((i, j))
        part2 += len(accessible_locs)
        for i, j in accessible_locs:
            grid[i, j] = '.'
        stop = len(accessible_locs) == 0
    print('Part 1:', part1)
    print('Part 2:', part2)
