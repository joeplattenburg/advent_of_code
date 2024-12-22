import sys
import networkx as nx
import numpy as np
from itertools import product


EDGES = dict[tuple[str, str], str]  # i.e., e[(node, neighbor)] gives the direction
PATH = list[str]
PATH_MAP = dict[str, dict[str, list[PATH]]]  # i.e., g[source][dest] gives several paths

num_pad = np.array([
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['X', '0', 'A']
])
dir_pad = np.array([
    ['X', '^', 'A'],
    ['<', 'v', '>'],
])


def parse_input(input_path) -> list[str]:
    with open(input_path, 'r') as f:
        out = [line.strip() for line in f.readlines()]
    return out


def get_edges(array: np.ndarray) -> EDGES:
    nodes = [n for n in np.unique(array) if n != 'X']
    out = {}
    for node in nodes:
        self_loc = tuple(np.argwhere(array == node)[0])
        for dir, di, dj in [('^', -1, 0), ('v', 1, 0), ('>', 0, 1), ('<', 0, -1)]:
            neighbor_loc = self_loc[0] + di, self_loc[1] + dj
            if (
                (0 <= neighbor_loc[0] < array.shape[0]) and
                (0 <= neighbor_loc[1] < array.shape[1]) and
                array[*neighbor_loc] != 'X'
            ):
                out[(str(array[*self_loc]), str(array[*neighbor_loc]))] = dir
    return out


def sequence_to_instructions(seq: str, path_map: PATH_MAP, key_map: EDGES, n: int = 1) -> str:
    instructions = []
    for source, dest in zip('A' + seq[:-1], seq):
        subpaths: list[PATH] = path_map[source][dest]
        dirs = [get_dirs(subpath, key_map) for subpath in subpaths]
        instructions.append(dirs)
        instructions.append(['A'])
    instructions = [''.join(i) for i in product(*instructions)]
    if n == 1:
        return min(instructions, key=len)
    else:
        return min([sequence_to_instructions(i, path_map=dir_paths, key_map=dir_edges, n=n-1) for i in instructions], key=len)


def get_dirs(path: PATH, key_map: EDGES) -> str:
    return ''.join(key_map[(source, dest)] for source, dest in zip(path[:-1], path[1:]))


if __name__ == "__main__":
    input_path = sys.argv[1]
    codes = parse_input(input_path)
    num_edges = get_edges(num_pad)
    dir_edges = get_edges(dir_pad)
    num_g = nx.DiGraph()
    num_g.add_edges_from(num_edges.keys())
    num_paths: PATH_MAP = {k: v for k, v in nx.all_pairs_all_shortest_paths(num_g)}
    dir_g = nx.Graph()
    dir_g.add_edges_from(dir_edges.keys())
    dir_paths: PATH_MAP = {k: v for k, v in nx.all_pairs_all_shortest_paths(dir_g)}
    part1 = 0
    for code in codes:
        inst = sequence_to_instructions(seq=code, path_map=num_paths, key_map=num_edges, n=3)
        print(inst)
        print(len(inst))
        part1 += len(inst) * int(code[:-1])
    part2 = 0
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
