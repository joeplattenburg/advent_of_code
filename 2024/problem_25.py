import sys
import numpy as np


def parse_input(input_path) -> tuple[list[np.ndarray], list[np.ndarray], int]:
    locks, keys = [], []
    with open(input_path, 'r') as f:
        grids = f.read().split('\n\n')
    for grid in grids:
        array = np.array([[c for c in line] for line in grid.split('\n')])
        space = array.shape[0] - 2
        if all(array[0, :] == '#'):
            locks.append((array == '#').sum(axis=0) - 1)
        else:
            keys.append((array == '#').sum(axis=0) - 1)
    return locks, keys, space


if __name__ == "__main__":
    input_path = sys.argv[1]
    locks, keys, space = parse_input(input_path)
    part1 = sum(all((lock + key) <= space) for key in keys for lock in locks)
    print(f'Part 1: {part1}')
    print(f'Part 2: Done!')
