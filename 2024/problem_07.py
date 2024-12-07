import sys
from itertools import product


def parse_line(line: str) -> tuple[int, list[int]]:
    left, right = line.split(':')
    result = int(left.strip())
    inputs = [int(r) for r in right.strip().split()]
    return result, inputs


def is_possible(result: int, inputs: list[int], operators: list[str], required: str | None = None) -> bool:
    operator_combs = list(product(operators, repeat=len(inputs) - 1))
    if required:
        operator_combs = [o for o in operator_combs if required in o]
    for operator_comb in operator_combs:
        if eval_statement(inputs, operator_comb) == result:
            return True
    return False


def eval_statement(inputs: list[int], operators: list[str]) -> str:
    value = inputs[0]
    for operator, next_value in zip(operators, inputs[1:]):
        value = eval(str(value) + operator + str(next_value))
    return value


if __name__ == "__main__":
    input_path = sys.argv[1]
    part1 = 0
    part2 = 0
    with open(input_path, 'r') as f:
        for line in f.readlines():
            result, inputs = parse_line(line.strip())
            if is_possible(result, inputs, operators=['*', '+']):
                part1 += result
                part2 += result
            elif is_possible(result, inputs, operators=['*', '+', ''], required=''):
                part2 += result
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
