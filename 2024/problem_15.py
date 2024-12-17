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
        inds_to_move = self.movable_inds(direction)
        if inds_to_move:
            grid_copy = deepcopy(self.grid)
            for ind in inds_to_move:
                self.grid[*ind] = '.'
            for ind in inds_to_move:
                new_ind = ind[0] + direction[0], ind[1] + direction[1]
                self.grid[*new_ind] = grid_copy[*ind]

    def movable_inds(self, direction: Coord, accumulated: list[Coord] | None = None, leading_edge_size: int = 1) -> list[Coord]:
        accumulated = accumulated or [self.robot_index()]
        leading_edge = accumulated[-leading_edge_size:]
        new_leading_edge = set()
        for coord in leading_edge:
            check_coord = coord[0] + direction[0], + coord[1] + direction[1]
            check_val = self.grid[*check_coord]
            # If there are any walls along the leading edge, nothing can move
            if check_val == '#':
                return []
            elif check_val == '.':
                continue
            elif check_val == 'O':
                new_leading_edge.add(check_coord)
            elif check_val == '[':
                # up or down, both halves of box are on leading edge
                if direction[1] == 0:
                    new_leading_edge.add(check_coord)
                    new_leading_edge.add((check_coord[0], check_coord[1] + 1))
                else:
                    accumulated.append(check_coord)
                    new_leading_edge.add((check_coord[0], check_coord[1] + 1))
            elif check_val == ']':
                if direction[1] == 0:
                    new_leading_edge.add(check_coord)
                    new_leading_edge.add((check_coord[0], check_coord[1] - 1))
                else:
                    accumulated.append(check_coord)
                    new_leading_edge.add((check_coord[0], check_coord[1] - 1))
        accumulated += list(new_leading_edge)
        if not new_leading_edge:
            return accumulated
        else:
            return self.movable_inds(direction, accumulated, leading_edge_size=len(new_leading_edge))

    def print_grid(self):
        for i in range(self.grid.shape[0]):
            print(''.join(self.grid[i, :].tolist()))

    def sum_coords(self) -> int:
        return sum(i * 100 + j for i, j in np.argwhere(np.isin(self.grid, ['O', '['])))


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
    grid2 = Grid(widen_grid(deepcopy(grid.grid)))
    #grid2.print_grid()
    for instruction in instructions:
        grid.update_grid(instruction)
        grid2.update_grid(instruction)
    #grid2.print_grid()
    print(f'Part 1: {grid.sum_coords()}')
    print(f'Part 2: {grid2.sum_coords()}')
