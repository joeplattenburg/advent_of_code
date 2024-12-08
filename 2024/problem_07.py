import sys
from operator import add, mul


def parse_line(line: str) -> tuple[int, list[int]]:
    left, right = line.split(':')
    result = int(left.strip())
    inputs = [int(r) for r in right.strip().split()]
    return result, inputs


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def is_possible(result: int, inputs: list[int], operators: list[callable]) -> bool:
    if len(inputs) == 1:
        if result == inputs[0]:
            return True
    else:
        for op in operators:
            new_val = op(inputs[0], inputs[1])
            if new_val > result:
                return False
            if is_possible(result, [new_val, *inputs[2:]], operators=operators):
                return True
    return False


if __name__ == "__main__":
    input_path = sys.argv[1]
    part1 = 0
    part2 = 0
    with open(input_path, 'r') as f:
        for line in f.readlines():
            result, inputs = parse_line(line.strip())
            if is_possible(result, inputs, operators=[add, mul]):
                part1 += result
            if is_possible(result, inputs, operators=[add, mul, concat]):
                part2 += result
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
