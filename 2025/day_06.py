import sys
import numpy as np


def pad_lines(lines: list[str]) -> list[str]:
    max_len = max(len(line) for line in lines)
    return [line + ' ' * (max_len - len(line)) for line in lines]


def parse(lines: list[str], part2: bool = False) -> list[str]:
    operators = lines[-1].split()
    split_indices = [i - 1 for i, val in enumerate(lines[-1]) if i > 0 and val != ' ']
    problems = []
    for op, i, j in zip(operators, [None, *split_indices], [*split_indices, None]):
        i = i + 1 if i is not None else i
        grid = np.array([list(line[i:j]) for line in lines[:-1]])
        if part2:
            grid = grid.transpose()
        problems.append(op.join(''.join(grid[k, :]).strip() for k in range(grid.shape[0])))
    return problems


if __name__ == "__main__":
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        lines = pad_lines(f.read().split('\n'))
    part1 = sum(eval(p) for p in parse(lines, part2=False))
    part2 = sum(eval(p) for p in parse(lines, part2=True))
    print('Part 1:', part1)
    print('Part 2:', part2)
