import sys
from dataclasses import dataclass


@dataclass
class Machine:
    a: complex
    b: complex
    prize: complex


def parse_input(path: str) -> list[Machine]:
    with open(path, 'r') as f:
        machines = f.read().strip().split('\n\n')
    out = []
    for m in machines:
        a, b, prize = m.split('\n', maxsplit=3)
        mm = Machine(a=parse_helper(a, '+'), b=parse_helper(b, '+'), prize=parse_helper(prize, '='))
        out.append(mm)
    return out


def get_solutions(m: Machine) -> list[tuple[int, int, int]]:
    out = []
    for i in range(100):
        for j in range(100):
            loc = i * m.a + j * m.b
            if loc == m.prize:
                out.append((i, j, i * 3 + j))
            elif abs(loc) > abs(m.prize):
                break
    return out


def parse_helper(s: str, char: str) -> complex:
    x, y = s.split(':')[1].split(',')
    return complex(int(x.strip().split(char)[1]), int(y.strip().split(char)[1]))


if __name__ == "__main__":
    input_path = sys.argv[1]
    machines = parse_input(input_path)
    part1, part2 = 0, 0
    for machine in machines:
        solutions = get_solutions(machine)
        if solutions:
            part1 += sorted(solutions, key=lambda x: x[2])[0][2]
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
