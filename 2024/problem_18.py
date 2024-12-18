import sys
import networkx as nx
from networkx.exception import NetworkXNoPath


def build_graph(memory_space: int, corrupted: set[tuple[int, int]]) -> nx.Graph:
    nodes = [
        (i, j)
        for i in range(memory_space)
        for j in range(memory_space)
        if (i, j) not in corrupted
    ]
    edges = [
        ((i, j), (i + di, j + dj))
        for (i, j) in nodes
        for (di, dj) in ((0, 1), (0, -1), (1, 0), (-1, 0))
        if (
            (i + di, j + dj) not in corrupted and
            0 <= i + di < memory_space and
            0 <= j + dj < memory_space
        )
    ]
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g


if __name__ == "__main__":
    input_path = sys.argv[1]
    memory_space, n_bytes = (7, 12) if input_path.endswith('0.txt') else (71, 1024)
    coords = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            i, j = line.strip().split(',')
            coords.append((int(i), int(j)))
    corrupted = set(coords[:n_bytes])
    source, target = (0, 0), (memory_space - 1, memory_space - 1)
    g = build_graph(memory_space, corrupted)
    path = nx.shortest_path(g, source, target)
    part1 = len(path) - 1

    blocked = False
    while not blocked:
        g.remove_node(coords[n_bytes])
        try:
            path = nx.shortest_path(g, source, target)
        except NetworkXNoPath:
            part2 = coords[n_bytes]
            blocked = True
        n_bytes += 1

    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
