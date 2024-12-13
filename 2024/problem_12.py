import sys
from collections import Counter, defaultdict
import numpy as np
from scipy.ndimage import label


def get_all_sides(inds: list[tuple[int, int]], grid: np.ndarray) -> list[tuple[tuple[int, int], complex]]:
    edges = []
    for ind in inds:
        self = grid[*ind]
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_ind = ind[0] + di, ind[1] + dj
            if not (on_grid(neighbor_ind, grid) and grid[*neighbor_ind] == self):
                edges.append((tuple(ind), complex(di, dj)))
    return edges


def get_perimeter(inds: list[tuple[int, int]], grid: np.ndarray) -> int:
    return len(get_all_sides(inds, grid))


def get_sides(inds: list[tuple[int, int]], grid: np.ndarray) -> int:
    all_sides = get_all_sides(inds, grid)
    sides = defaultdict(list)
    for (si, sj), direc in all_sides:
        if direc.real != 0:
            sides[(si, direc)].append(sj)
        else:
            sides[(sj, direc)].append(si)
    return sum(sum(np.diff(np.array(sorted(s))) > 1) + 1 for s in sides.values())


def on_grid(ind: tuple[int, int], grid: np.ndarray) -> bool:
    return (0 <= ind[0] < grid.shape[0]) and (0 <= ind[1] < grid.shape[1])


def get_regions(grid: np.ndarray) -> dict[tuple[str, int], list[tuple[int, int]]]:
    regions = np.unique(grid)
    out = {}
    for r in regions:
        inds, n_regions = label(grid == r)
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
    locs = get_regions(grid)
    part1, part2 = 0, 0
    for (region, i), inds in locs.items():
        part1 += len(inds) * get_perimeter(inds, grid)
        part2 += len(inds) * get_sides(inds, grid)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
