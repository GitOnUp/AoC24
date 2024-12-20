import re
from dataclasses import dataclass


ROBOT_PATTERN = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")


@dataclass
class Robot:
    pos: (int, int)
    vel: (int, int)


def read_input():
    robots = []
    with open("p14.input.txt", "r") as f:
        for line in f.readlines():
            match = ROBOT_PATTERN.match(line)
            x = int(match.group(1))
            y = int(match.group(2))
            dx = int(match.group(3))
            dy = int(match.group(4))
