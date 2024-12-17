import sys
from collections import defaultdict

import networkx as nx
import numpy as np


Node = tuple[int, int, complex]
Edge = tuple[Node, Node]

direction_mapper = {
    complex(1, 0): '>',
    complex(-1, 0): '<',
    complex(0, 1): '^',
    complex(0, -1): 'v'
}


def parse_input(input_path) -> np.ndarray:
    out = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            out.append([c for c in line.strip()])
    return np.array(out)


def get_edges(nodes: list[Node]) -> dict[Edge, int]:
    out = {}
    for node in nodes:
        left = (node[0], node[1], node[2] * complex(0, 1))
        right = (node[0], node[1], node[2] * complex(0, -1))
        out[(node, left)] = 1000
        out[(node, right)] = 1000
        neighbor = int(node[0] - node[2].imag), int(node[1] + node[2].real), node[2]
        if neighbor in nodes:
            out[(node, neighbor)] = 1
    return out


def get_score(path: list[Node], weights: dict[Edge, int]) -> int:
    return sum(weights[(start, end)] for start, end in zip(path[:-1], path[1:]))


if __name__ == "__main__":
    input_path = sys.argv[1]
    maze = parse_input(input_path)
    start_node, end_node = tuple(np.argwhere(maze == 'S').tolist()[0]), tuple(np.argwhere(maze == 'E').tolist()[0])
    inter = [(int(i), int(j)) for i, j in np.argwhere(maze == '.')]
    all_nodes = [
        (i, j, direction)
        for i, j in [start_node, *inter, end_node]
        for direction in direction_mapper.keys()
    ]
    edges = get_edges(all_nodes)
    g = nx.DiGraph()
    g.add_nodes_from(all_nodes)
    g.add_edges_from([(i, j, {'weight': w}) for (i, j), w in edges.items()])
    start = (start_node[0], start_node[1], complex(1, 0))
    ends = [(end_node[0], end_node[1], direction) for direction in direction_mapper.keys()]
    paths = []
    for end in ends:
        paths += list(nx.all_shortest_paths(g, start, end, weight='weight'))
    scores = defaultdict(list)
    for path in paths:
        scores[get_score(path, weights=edges)].append(path)
    min_score = min(scores.keys())
    optimal_paths = scores[min_score]
    optimal_nodes = set()
    for path in optimal_paths:
        for node in path:
            optimal_nodes.add((node[0], node[1]))
    part1 = min_score
    part2 = len(optimal_nodes)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
