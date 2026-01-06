import sys
from functools import cache


def parse_line(s: str) -> tuple[str, list[str]]:
    k, v = s.split(':')
    return k.strip(), v.strip().split()


@cache
def count_paths(start: str, end: str = 'out', **seen_keys) -> int:
    n = 0
    for next_ in graph[start]:
        if next_ == end:
            return all(seen_keys.values()) if seen_keys else 1
        else:
            next_seen_keys = {key: seen | (key == next_) for key, seen in seen_keys.items()}
            n += count_paths(start=next_, **next_seen_keys)
    return n


if __name__ == "__main__":
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        graph = dict(parse_line(line.strip()) for line in f.readlines())
    part1 = count_paths(start='you')
    part2 = count_paths(start='svr', fft=False, dac=False)
    print('Part 1:', part1)
    print('Part 2:', part2)
