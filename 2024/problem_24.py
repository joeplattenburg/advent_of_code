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


def validate_ops(i: int, ci: str, swaps: list[tuple[str, str]]) -> int | None:
    # expected operation for addition
    # x XOR y -> a
    # x AND y -> b
    # ci XOR a -> z
    # ci AND a -> d
    # b OR d -> co
    xi, yi, zi = f'x{i:02}', f'y{i:02}', f'z{i:02}'
    a = safe_get_op(xi, 'XOR', yi)
    b = safe_get_op(xi, 'AND', yi)
    if ci:
        d = safe_get_op(ci, 'AND', a)
        co = safe_get_op(b, 'OR', d)
        z = safe_get_op(ci, 'XOR', a)
        for val in (a, b, d, co):
            if val == zi:
                swap(val, z)
                swaps.append((val, z))
                return validate_ops(i, ci, swaps)
        if d is None:
            swap(a, b)
            swaps.append((a, b))
            return validate_ops(i, ci, swaps)
    else:
        z = a
        co = b
    assert z == zi
    return co


def safe_get_op(a: str, op: OPS, b: str) -> str | None:
    out = gates_inv.get((a, op, b)) or gates_inv.get((b, op, a))
    return out


def swap(a: str, b: str) -> None:
    a_key = gates[a]
    b_key = gates[b]
    gates_inv[a_key] = b
    gates_inv[b_key] = a


if __name__ == "__main__":
    input_path = sys.argv[1]
    values, gates = parse_input(input_path)
    n_bits = len(values) // 2

    for k, v in gates.items():
        values[k] = do_op(*v)
    outputs = sorted(
        [(k, v) for k, v in values.items() if k.startswith('z')],
        key=lambda x: x[0], reverse=True
    )
    part1 = int(''.join(str(o[1]) for o in outputs), 2)

    gates_inv = {(a, op, b): out for out, (a, op, b) in gates.items()}
    swaps = []
    ci = ''
    for i in range(n_bits):
        ci = validate_ops(i, ci, swaps)
    part2 = ','.join(sorted([ss for s in swaps for ss in s]))
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
