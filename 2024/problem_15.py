import sys
from copy import deepcopy

import numpy as np

Coord = tuple[int, int]


class Grid:
    instruction_map = {'v': (1, 0), '^': (-1, 0), '>': (0, 1), '<': (0, -1)}
    def __init__(self, grid: np.ndarray):
        self.grid = grid

    def robot_index(self) -> Coord:
        return tuple(np.argwhere(self.grid == '@')[0])

    def update_grid(self, instruction: str) -> None:
        direction = self.instruction_map[instruction]
        current_loc = self.robot_index()
        inds_to_move = self.movable_inds(direction)
        if inds_to_move:
            for ind in reversed(inds_to_move):
                new_ind = ind[0] + direction[0], ind[1] + direction[1]
                self.grid[*new_ind] = self.grid[*ind]
            self.grid[*current_loc] = '.'

    def movable_inds(self, direction: Coord, accumulated: list[Coord] | None = None) -> list[Coord]:
        accumulated = accumulated or [self.robot_index()]
        leading_edge = self.get_leading_edge(accumulated, direction)
        current_coord = leading_edge[0]
        check_coord = current_coord[0] + direction[0], + current_coord[1] + direction[1]
        check_val = self.grid[*check_coord]
        if check_val == '#':
            return []
        elif check_val == '.':
            return accumulated
        else:
            accumulated.append(check_coord)
            return self.movable_inds(direction, accumulated)

    @staticmethod
    def get_leading_edge(coords: list[Coord], direction: Coord) -> list[Coord]:
        return [coords[-1]]

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


def widen_grid(grid: np.ndarray) -> np.ndarray:
    mapper = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
    new_grid = np.empty(shape=(grid.shape[0], 2 * grid.shape[1]), dtype=str)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            old = grid[i, j]
            new = mapper[old]
            new_grid[i, 2 * j] = new[0]
            new_grid[i, 2 * j + 1] = new[1]
    return new_grid


if __name__ == "__main__":
    input_path = sys.argv[1]
    grid, instructions = parse_input(input_path)
    grid.print_grid()
    for i, instruction in enumerate(instructions):
        grid.update_grid(instruction)
    grid.print_grid()
    print(f'Part 1: {grid.sum_coords()}')
