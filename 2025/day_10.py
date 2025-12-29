import sys
from typing import TypeVar
from itertools import chain, combinations

A = TypeVar('A')


def parse_line(line: str) -> tuple[str, list[tuple[int, ...]], list[int]]:
    line = line.replace('[', '').replace('}', '')
    lights, temp = line.split(']')
    lights = lights.replace('.', '0').replace('#', '1')
    buttons, joltage = temp.split('{')
    buttons = [
        tuple(int(i) for i in b.split(','))
        for b in buttons.strip().replace('(', '').replace(')', '').split()
    ]
    joltage = [int(i) for i in joltage.split(',')]
    return lights, buttons, joltage


def powerset(s: set[A]) -> list[set[A]]:
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def press_buttons(buttons: set[tuple[int, ...]], n: int) -> str:
    lights = [0] * n
    for b in buttons:
        for i in b:
            lights[i] = (lights[i] + 1) % 2
    return ''.join(str(i) for i in lights)


if __name__ == "__main__":
    input_path = sys.argv[1]
    part1, part2 = 0, 0
    with open(input_path, 'r') as f:
        for line in f.readlines():
            lights, buttons, joltage = parse_line(line.strip())
            for b in powerset(set(buttons)):
                if press_buttons(b, n=len(lights)) == lights:
                    part1 += len(b)
                    break
    print('Part 1:', part1)
    print('Part 2:', part2)
