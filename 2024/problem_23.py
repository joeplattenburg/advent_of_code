import sys
from collections import defaultdict


def parse_input(input_path) -> list[tuple[int, int]]:
    out = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            a, b = line.strip().split('-')
            out.append((a, b))
    return out


if __name__ == "__main__":
    input_path = sys.argv[1]
    edges = parse_input(input_path)
    triples = set()
    pairs = defaultdict(set)
    for a, b in edges:
        pairs[a].add(b)
        pairs[b].add(a)
    for node, neighbors in pairs.items():
        for neighbor in neighbors:
            intersection = neighbors.intersection(pairs[neighbor])
            for other in intersection:
                triple = (node, neighbor, other)
                triples.add(tuple(sorted(triple)))
    part1 = sum(any(n.startswith('t') for n in t) for t in triples)
    part2 = 0
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
