import sys
from typing import Literal


OPS = Literal['AND', 'OR', 'XOR']
GATE = dict[str, tuple[str, OPS, str]]


def parse_input(input_path) -> tuple[dict[str, int], GATE]:
    values = {}
    gates = {}
    with open(input_path, 'r') as f:
        values_s, gates_s = f.read().split('\n\n')
    for value in values_s.split('\n'):
        k, v = value.strip().split(': ')
        values[k] = int(v)
    for gate in gates_s.split('\n'):
        a, op, b, _, out = gate.strip().split(maxsplit=4)
        gates[out] = (a, op, b)
    return values, gates


def do_op(a_s: str, op: OPS, b_s: str) -> int:
    a = values[a_s] if a_s in values else do_op(*gates[a_s])
    b = values[b_s] if b_s in values else do_op(*gates[b_s])
    if op == 'AND':
        return a & b
    elif op == 'OR':
        return a | b
    elif op == 'XOR':
        return a ^ b


if __name__ == "__main__":
    input_path = sys.argv[1]
    values, gates = parse_input(input_path)
    for k, v in gates.items():
        values[k] = do_op(*v)
    outputs = sorted(
        [(k, v) for k, v in values.items() if k.startswith('z')],
        key=lambda x: x[0], reverse=True
    )
    part1 = int(''.join(str(o[1]) for o in outputs), 2)
    part2 = 0
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
