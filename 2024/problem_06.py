from copy import deepcopy
import sys
import numpy as np


class Grid:
    directions = ['^', '>', 'v', '<']

    def __init__(self, grid: np.ndarray) -> None:
        starting_loc_ind = (grid == '^') | (grid == 'v') | (grid == '<') | (grid == '>')
        assert starting_loc_ind.sum() == 1
        self.direction: str = str(grid[starting_loc_ind][0])
        x, y = np.where(starting_loc_ind)
        self.loc = int(x[0]), int(y[0])
        self.history = [(self.loc, self.direction)]
        self.unique_states = {(self.loc, self.direction)}
        self.grid = grid
        self.original_grid = deepcopy(grid)
        self.loc_on_grid = True
        self.loop = False

    def take_step(self) -> None:
        if self.direction == '^':
            test_loc = self.loc[0] - 1, self.loc[1]
        elif self.direction == 'v':
            test_loc = self.loc[0] + 1, self.loc[1]
        elif self.direction == '>':
            test_loc = self.loc[0], self.loc[1] + 1
        elif self.direction == '<':
            test_loc = self.loc[0], self.loc[1] - 1
        else:
            raise Exception('wat')
        if self.is_loc_on_grid(test_loc):
            if self.grid[*test_loc] == '#':
                self.turn_right()
            else:
                self.grid[*self.loc] = 'X'
                self.loc = test_loc
            self.grid[*self.loc] = self.direction
            if (self.loc, self.direction) in self.unique_states:
                self.loop = True
            self.history.append((self.loc, self.direction))
            self.unique_states.add((self.loc, self.direction))
        else:
            self.grid[*self.loc] = 'X'
            self.loc_on_grid = False
            self.loc = None

    def is_loc_on_grid(self, loc: tuple[int, int]) -> bool:
        return (loc[0] >= 0) and (loc[0] < self.grid.shape[0]) and (loc[1] >= 0) and (loc[1] < self.grid.shape[1])

    def turn_right(self):
        self.direction = self.directions[(self.directions.index(self.direction) + 1) % len(self.directions)]

    def print(self) -> None:
        for i in range(self.grid.shape[0]):
            print(''.join(self.grid[i, :]))

    def count_locations(self) -> int:
        return int((self.grid == 'X').sum())

    def walk(self):
        while self.loc_on_grid and not self.loop:
            self.take_step()

    def reset(self):
        self.loc, self.direction = self.history[0]
        self.history = [(self.loc, self.direction)]
        self.unique_states = {(self.loc, self.direction)}
        self.grid = deepcopy(self.original_grid)
        self.loc_on_grid = True
        self.loop = False


if __name__ == "__main__":
    input_path = sys.argv[1]
    array = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            array.append([c for c in line.strip()])
    grid = Grid(np.array(array))
    grid.walk()
    part1 = grid.count_locations()

    part2 = 0
    test_locs = [tuple(t) for t in np.argwhere(grid.grid == 'X').tolist()]
    for i, loc in enumerate(test_locs):
        print(f'Testing loc {i + 1} of {len(test_locs)}...')
        grid.reset()
        grid.grid[*loc] = '#'
        grid.walk()
        if grid.loop:
            part2 += 1
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
