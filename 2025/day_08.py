import sys
import math
from itertools import combinations
from functools import reduce, total_ordering
from dataclasses import dataclass


@total_ordering
@dataclass
class Coord:
    vals: tuple[int, ...]

    @classmethod
    def parse(cls, s: str) -> 'Coord':
        return cls(vals=tuple([int(i) for i in s.split(',')]))

    def distance(self, other: 'Coord') -> float:
        return math.sqrt(sum((aa - bb) ** 2 for aa, bb in zip(self.vals, other.vals)))

    def __eq__(self, other):
        return self.vals == other.vals

    def __lt__(self, other):
        return self.vals < other.vals

    def __hash__(self):
        return hash(self.vals)


@total_ordering
@dataclass
class Component:
    coords: set[Coord]

    def union(self, other: 'Component'):
        return Component(coords=(self.coords | other.coords))

    def __contains__(self, coord: Coord) -> bool:
        return coord in self.coords

    def __hash__(self):
        return hash(tuple(sorted(list(self.coords))))

    def __len__(self):
        return len(self.coords)

    def __eq__(self, other) -> bool:
        return len(self.coords) == len(other.coords)

    def __lt__(self, other) -> bool:
        return len(self.coords) < len(other.coords)


if __name__ == "__main__":
    input_path = sys.argv[1]
    part1, part2 = 0, 0
    with open(input_path, 'r') as f:
        coords = sorted([Coord.parse(line.strip()) for line in f.readlines()])
    components = [Component(coords={c}) for c in coords]
    dists = dict(sorted(
        {(a, b): a.distance(b) for a, b in combinations(coords, 2)}.items(),
        key=lambda x: x[1]
    ))
    for i, (pair, dist) in enumerate(dists.items()):
        new_components = []
        components_to_connect = set()
        for comp in components:
            if (pair[0] not in comp) and (pair[1] not in comp):
                new_components.append(comp)
            else:
                if pair[0] in comp:
                    components_to_connect.add(comp)
                if pair[1] in comp:
                    components_to_connect.add(comp)
        connected_comp = reduce(lambda x, y: x.union(y), components_to_connect)
        new_components.append(connected_comp)
        components = new_components
        if i + 1 == 1000:
            part1 = math.prod(len(c) for c in sorted(components, reverse=True)[:3])
        if len(components) == 1:
            part2 = pair[0].vals[0] * pair[1].vals[0]
            break
    print(len(components))
    print('Part 1:', part1)
    print('Part 2:', part2)
