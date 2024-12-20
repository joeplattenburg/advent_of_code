import sys
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

def get_neighbors_within_n(node: Node, n: int = 2) -> set[Node]:
    return set(
        (node[0] + di, node[1] + dj)
        for di, dj in (
            (0, 1), (0, 2), (0, -1), (0, -2),
            (1, 0), (2, 0), (-1, 0), (-2, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1),
        )
    )


if __name__ == "__main__":
    input_path = sys.argv[1]
    maze = parse_input(input_path)
    start_node, end_node = tuple(np.argwhere(maze == 'S').tolist()[0]), tuple(np.argwhere(maze == 'E').tolist()[0])
    inter = [(int(i), int(j)) for i, j in np.argwhere(maze == '.')]
    all_nodes = {start_node, *inter, end_node}
    edges = get_edges(new_nodes=all_nodes, all_nodes=all_nodes, shape=maze.shape)
    g = nx.Graph()
    g.add_nodes_from(all_nodes)
    g.add_edges_from(edges)
    fair_path = nx.shortest_path(g, start_node, end_node)
    cumulative_time = {node: i for i, node in enumerate(fair_path)}
    cheats = {}
    for node, time in cumulative_time.items():
        neighbors = get_neighbors_within_n(node)
        for neighbor in neighbors:
            if (subpath := cumulative_time.get(neighbor, 0) - time) > 2:
                cheats[(node, neighbor)] = subpath - 2
    cheat_summary = Counter(cheats.values())
    part1 = sum(v for k, v in cheat_summary.items() if k >= 100)
    part2 = 0
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
