import sys


def parse_instruction(i: str) -> int:
    return {'L': -1, 'R': 1}[i[0]] * int(i[1:])


if __name__ == "__main__":
    input_path = sys.argv[1]
    current = 50
    part1 = 0
    part2 = 0
    with (open(input_path, 'r') as f):
        for line in f.readlines():
            instruction = parse_instruction(line.strip())
            if current == 0 and instruction < 0:
                current = 100
            current += instruction
            part2 += abs(current // 100)
            current %= 100
            if instruction < 0:
                part2 += int(current == 0)
            part1 += int(current == 0)
    print('Part 1:', part1)
    print('Part 2:', part2)
