from copy import deepcopy
import sys
import numpy as np


class LoopError(Exception):
    pass


class Grid:
    directions = ['^', '>', 'v', '<']

    def __init__(self, grid: np.ndarray) -> None:
        starting_loc_ind = (grid == '^') | (grid == 'v') | (grid == '<') | (grid == '>')
        assert starting_loc_ind.sum() == 1
        self.direction: str = str(grid[starting_loc_ind][0])
        x, y = np.where(starting_loc_ind)
        self.loc = int(x[0]), int(y[0])
        self.grid = grid
        self.loc_on_grid = True

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

    def open_locations(self) -> list[tuple[int, int]]:
        return [tuple(t) for t in np.argwhere(self.grid == '.').tolist()]

    def walk(self, cutoff=100000):
        counter = 0
        while self.loc_on_grid:
            self.take_step()
            counter += 1
            if counter >= cutoff:
                raise LoopError


if __name__ == "__main__":
    input_path = sys.argv[1]
    original_array = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            original_array.append([c for c in line.strip()])
    original_array = np.array(original_array)
    grid = Grid(deepcopy(original_array))
    grid.walk()
    part1 = grid.count_locations()
    print('Part 1 done')

    part2 = 0
    grid = Grid(original_array)
    open_locs = grid.open_locations()
    for i, loc in enumerate(grid.open_locations()):
        print(f'Testing loc {i + 1} of {len(open_locs)}...')
        new_array = deepcopy(original_array)
        new_array[*loc] = '#'
        new_grid = Grid(new_array)
        try:
            new_grid.walk(cutoff=100000)
        except LoopError:
            part2 += 1
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
