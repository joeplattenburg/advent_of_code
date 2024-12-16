import sys

import numpy as np


class Grid:
    instruction_map = {'v': (1, 0), '^': (-1, 0), '>': (0, 1), '<': (0, -1)}
    def __init__(self, grid: np.ndarray):
        self.grid = grid

    def robot_index(self) -> tuple[int, int]:
        return tuple(np.argwhere(self.grid == '@')[0])

    def update_grid(self, instruction: str) -> None:
        direction = self.instruction_map[instruction]
        start = self.robot_index()
        end = self.get_first_non_box(direction)
        if self.grid[*end] == '.':
            if instruction == '>':
                self.grid[start[0], (start[1] + 1):(end[1] + 1)] = self.grid[start[0], start[1]:end[1]]
            elif instruction == '<':
                end1 = end[1] - 1 if end[1] - 1 >= 0 else None
                self.grid[start[0], (start[1] - 1):end1:-1] = self.grid[start[0], start[1]:end[1]:-1]
            elif instruction == 'v':
                self.grid[(start[0] + 1):(end[0] + 1), start[1]] = self.grid[start[0]:end[0], start[1]]
            elif instruction == '^':
                end1 = end[0] - 1 if end[0] - 1 >= 0 else None
                self.grid[(start[0] - 1):end1:-1, start[1]] = self.grid[start[0]:(end[0]):-1, start[1]]
            self.grid[*start] = '.'

    def get_first_non_box(self, direction: tuple[int, int]) -> tuple[int, int]:
        loc = self.robot_index()
        stop = False
        while not stop:
            loc = loc[0] + direction[0], + loc[1] + direction[1]
            if self.grid[*loc] != 'O':
                stop = True
        return loc

    def print_grid(self):
        for i in range(self.grid.shape[0]):
            print(''.join(self.grid[i, :].tolist()))

    def sum_coords(self) -> int:
        return sum(i * 100 + j for i, j in np.argwhere(self.grid == 'O'))

def parse_input(input_path: str) -> tuple[Grid, str]:
    with open(input_path, 'r') as f:
        grid_string, instructions = f.read().split('\n\n')
    grid = []
    for line in grid_string.split('\n'):
        grid.append([c for c in line.strip()])
    return Grid(np.array(grid)), instructions.strip().replace('\n', '')


if __name__ == "__main__":
    input_path = sys.argv[1]
    grid, instructions = parse_input(input_path)
    grid.print_grid()
    for i, instruction in enumerate(instructions):
        grid.update_grid(instruction)
    grid.print_grid()
    print(f'Part 1: {grid.sum_coords()}')
