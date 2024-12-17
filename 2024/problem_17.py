import sys


def parse_input(input_path) -> tuple[dict[str, int], list[int]]:
    registers = {}
    with open(input_path, 'r') as f:
        for line in f.readlines():
            line_ = line.strip()
            if line_:
                type_, val = line.split(':')
                if type_.startswith('Register'):
                    registers[type_.split()[1]] = int(val)
                elif type_.startswith('Program'):
                    program = [int(v) for v in val.split(',')]
    return registers, program


def combo(val, registers: dict[str, int]) -> int:
    if val <= 3:
        return val
    elif val == 4:
        return registers['A']
    elif val == 5:
        return registers['B']
    elif val == 6:
        return registers['C']


def do_instruction(opcode: int, operand: int, registers: dict[str, int]) -> int | None:
    output = None
    if opcode == 0:  # adv
        registers['A'] = registers['A'] // (2 ** combo(operand, registers))
    elif opcode == 1:  #bxl
        registers['B'] = registers['B'] ^ operand
    elif opcode == 2:  #bst
        registers['B'] = combo(operand, registers) % 8
    elif opcode == 3:  #jnz
        if registers['A'] != 0:
            registers['pointer'] = operand
            return
    elif opcode == 4:  #bxc
        registers['B'] = registers['B'] ^ registers['C']
    elif opcode == 5:  #out
        output = combo(operand, registers) % 8
    elif opcode == 6:  #bdv
        registers['B'] = registers['A'] // (2 ** combo(operand, registers))
    elif opcode == 7:  #cdv
        registers['C'] = registers['A'] // (2 ** combo(operand, registers))
    registers['pointer'] += 2
    return output


if __name__ == "__main__":
    input_path = sys.argv[1]
    registers, program = parse_input(input_path)
    registers['pointer'] = 0
    halt = False
    outputs = []
    counter = 0
    while not halt:
        opcode, operand = program[registers['pointer']], program[registers['pointer'] + 1]
        output = do_instruction(opcode, operand, registers)
        if output is not None:
            outputs.append(output)
        halt = registers['pointer'] >= len(program)
        counter += 1
    part1 = ','.join(str(o) for o in outputs)
    part2 = 0
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
