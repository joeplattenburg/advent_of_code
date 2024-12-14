import sys
from collections import Counter
from math import prod


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


def count_quatrants(screen_size: tuple[int, int], locs: dict[tuple[int, int], int]) -> int:
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
    print(quadrants)
    return prod(quadrants.values())


if __name__ == "__main__":
    input_path = sys.argv[1]
    robots = {}
    with open(input_path, 'r') as f:
        for i, line in enumerate(f.readlines()):
            robots[i] = Robot.from_string(line)
    part1, part2 = 0, 0
    screen_size = (101, 103)
    for i, robot in robots.items():
        robot.move(duration=100, screen_size=screen_size)
    locs = Counter(robot.position for robot in robots.values())
    part1 = count_quatrants(screen_size, locs)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')
