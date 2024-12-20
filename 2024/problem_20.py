import sys
from copy import deepcopy
from collections import Counter

import networkx as nx
import numpy as np

Node = tuple[int, int]
Edge = tuple[Node, Node]


def parse_input(input_path) -> np.ndarray:
    out = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            out.append([c for c in line.strip()])
    return np.array(out)


def get_edges(new_nodes: set[Node], all_nodes: set[Node], shape: tuple[int, int]) -> set[Edge]:
    return set(
        ((i, j), (i + di, j + dj))
        for (i, j) in new_nodes
        for (di, dj) in ((0, 1), (0, -1), (1, 0), (-1, 0))
        if (
                (i + di, j + dj) in all_nodes and
                0 <= i + di < shape[0] and
                0 <= j + dj < shape[1]
        )
    )


if __name__ == "__main__":
    input_path = sys.argv[1]
    maze = parse_input(input_path)
    start_node, end_node = tuple(np.argwhere(maze == 'S').tolist()[0]), tuple(np.argwhere(maze == 'E').tolist()[0])
    inter = [(int(i), int(j)) for i, j in np.argwhere(maze == '.')]
    all_nodes = {start_node, *inter, end_node}
    walls = set((int(i), int(j)) for i, j in np.argwhere(maze == '#'))
    edges = get_edges(new_nodes=all_nodes, all_nodes=all_nodes, shape=maze.shape)
    g = nx.Graph()
    g.add_nodes_from(all_nodes)
    g.add_edges_from(edges)
    fair_path = nx.shortest_path(g, start_node, end_node)
    fair_time = len(fair_path) - 1
    cheat_locs = set(
        (i + di, j + dj)
        for i, j in fair_path
        for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0))
        if (
            (i + di, j + dj) in walls
            and 0 < (i + di) < (maze.shape[0] - 1)
            and 0 < (j + dj) < (maze.shape[1] - 1)
        )
    )
    cheat_times = {}
    for i, cheat in enumerate(cheat_locs):
        print(f'Testing {i} of {len(cheat_locs)}...')
        g_test = deepcopy(g)
        new_edges = get_edges(new_nodes={cheat}, all_nodes=all_nodes, shape=maze.shape)
        if len(new_edges) > 1:
            g_test.add_edges_from(new_edges)
            cheat_times[cheat] = fair_time - (len(nx.shortest_path(g_test, start_node, end_node)) - 1)
    cheat_summary = Counter(cheat_times.values())
    print(cheat_summary)
    part1 = sum(v for k, v in cheat_summary.items() if k >= 100)
    part2 = 0
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
