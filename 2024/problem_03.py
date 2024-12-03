import sys
import re


def compute_instruction(instruction: str) -> int:
    left, right = instruction.replace('mul(', '').replace(')', '').split(',')
    return int(left) * int(right)


def get_do_chunks(input_: str) -> list[str]:
    do_chunks = input_.split('do()')
    return [c.split("don't()")[0] for c in do_chunks]


if __name__ == "__main__":
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        input_ = f.read().strip()

    pattern = re.compile("mul[(][0-9]{1,3},[0-9]{1,3}[)]")
    all_instructions = re.findall(pattern, input_)
    result1 = sum(compute_instruction(i) for i in all_instructions)

    do_chunks = get_do_chunks(input_)
    do_instructions = []
    for c in do_chunks:
        do_instructions += re.findall(pattern, c)
    result2 = sum(compute_instruction(i) for i in do_instructions)

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')
