import sys
from math import prod
from collections import Counter

import numpy as np


class Robot:
    def __init__(self, position: tuple[int, int], velocity: tuple[int, int]):
        self.position = position
        self.velocity = velocity

    def move(self, duration: int, screen_size: tuple[int, int]) -> None:
        self.position = (
            (self.position[0] + (self.velocity[0] * duration)) % screen_size[0],
            (self.position[1] + (self.velocity[1] * duration)) % screen_size[1],
        )

    @staticmethod
    def from_string(s: str) -> 'Robot':
        p, v = s.strip().split()
        px, py = p.split('=')[1].split(',')
        vx, vy = v.split('=')[1].split(',')
        return Robot((int(px), int(py)), (int(vx), int(vy)))


def count_quadrants(screen_size: tuple[int, int], locs: dict[tuple[int, int], int]) -> int:
    quadrants = {i: 0 for i in range(4)}
    for loc, count in locs.items():
        if loc[0] < (screen_size[0] // 2):
            if loc[1] < (screen_size[1] // 2):
                quadrants[0] += count
            elif loc[1] > (screen_size[1] // 2):
                quadrants[1] += count
        elif loc[0] > (screen_size[0] // 2):
            if loc[1] < (screen_size[1] // 2):
                quadrants[2] += count
            elif loc[1] > (screen_size[1] // 2):
                quadrants[3] += count
    return prod(quadrants.values())


def print_screen(screen: np.ndarray, counter: int) -> bool:
    check = any(['0000000000' in ''.join(screen[i, :].tolist()) for i in range(screen.shape[0])])
    # if check:
    #     for i in range(screen.shape[0]):
    #         print(''.join(screen[i, :].tolist()))
    return check


if __name__ == "__main__":
    input_path = sys.argv[1]
    robots = []
    with open(input_path, 'r') as f:
        for line in f.readlines():
            robots.append(Robot.from_string(line))
    screen_size = (101, 103)
    counter = 0
    found = False
    while not found:
        if counter == 100:
            locs = Counter(robot.position for robot in robots)
            part1 = count_quadrants(screen_size, locs)
        screen = np.full((screen_size[1], screen_size[0]), '.')
        for robot in robots:
            screen[robot.position[1], robot.position[0]] = '0'
        found = print_screen(screen, counter)
        if found:
            part2 = counter
        for robot in robots:
            robot.move(duration=1, screen_size=screen_size)
        counter += 1
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
