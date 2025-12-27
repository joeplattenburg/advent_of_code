import sys
import numpy as np
from collections import defaultdict


if __name__ == "__main__":
    input_path = sys.argv[1]
    part1, part2 = 0, 0
    with open(input_path, 'r') as f:
        grid = np.array([list(line.strip()) for line in f.readlines()])
    row, start_col = next(zip(*np.where(grid == 'S')))
    cols = {start_col: 1}
    for row in range(row + 1, grid.shape[1]):
        new_cols = defaultdict(int)
        for col, card in cols.items():
            if grid[row, col] == '^':
                part1 += 1
                new_cols[col - 1] += card
                new_cols[col + 1] += card
            else:
                new_cols[col] += card
        cols = new_cols
    print('Part 1:', part1)
    print('Part 2:', sum(cols.values()))
