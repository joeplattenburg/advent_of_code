import sys
import numpy as np
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


def decompose_into_basis(a: complex, b: complex, v: complex) -> tuple[float, float]:
    A = np.array([[a.real, b.real], [a.imag, b.imag]])
    V = np.array([v.real, v.imag])
    aa, bb = np.linalg.solve(A, V)
    return float(aa), float(bb)


def decompose_into_basis_(a: complex, b: complex, v: complex) -> tuple[float, float]:
    b_coef = (v.imag - (a.imag / a.real) * v.real) / (b.imag - b.real * (a.imag / a.real))
    a_coef = (v.real - b.real * b_coef) / a.real
    return a_coef, b_coef


def is_valid(t: tuple[float, float]) -> bool:
    return t[0] > 0 and t[1] > 0 and (abs(t[0] - np.round(t[0])) < 1e-8) and (abs(t[1] - np.round(t[1])) < 1e-8)


def parse_helper(s: str, char: str) -> complex:
    x, y = s.split(':')[1].split(',')
    return complex(int(x.strip().split(char)[1]), int(y.strip().split(char)[1]))


if __name__ == "__main__":
    input_path = sys.argv[1]
    machines = parse_input(input_path)
    part1, part2 = 0, 0
    for machine in machines:
        solution1 = decompose_into_basis_(machine.a, machine.b, machine.prize)
        if is_valid(solution1):
            part1 += int(np.round(solution1[0]) * 3 + np.round(solution1[1]))
        solution2 = decompose_into_basis_(machine.a, machine.b, machine.prize + complex(10000000000000, 10000000000000))
        if is_valid(solution2):
            part2 += int(np.round(solution2[0]) * 3 + np.round(solution2[1]))
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
