import sys
import numpy as np
from scipy.ndimage import label


def get_perimeter(inds: list[tuple[int, int]], grid: np.ndarray) -> int:
    out = 0
    for ind in inds:
        self = grid[*ind]
        for neighbor_ind in get_neighbor_inds(*ind):
            try:
                neighbor = grid[*neighbor_ind]
                out += int(neighbor != self)
            except IndexError:
                out += 1
    return out


def get_neighbor_inds(i: int, j: int) -> list[tuple[int, int]]:
    return [(i + di, j + dj) for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]]


def split_locs(regions: list[str], grid: np.ndarray):
    out = {}
    for r in regions:
        inds, n_regions = label(grid == r)
        #print(inds)
        for rr in range(n_regions):
            out[(r, rr)] = np.argwhere(inds == (rr + 1)).tolist()
    return out


if __name__ == "__main__":
    input_path = sys.argv[1]
    grid = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            grid.append([c for c in line.strip()])
    grid = np.array(grid)
    #locs = {region: np.argwhere(grid == region).tolist() for region in np.unique(grid)}
    locs = split_locs(np.unique(grid), grid)
    part1 = 0
    for (region, _), inds in locs.items():
        score = len(inds) * get_perimeter(inds, grid)
        #print(region, score)
        part1 += score
    part2 = 0
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
