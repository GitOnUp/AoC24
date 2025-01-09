import re
from dataclasses import dataclass
from pathlib import Path

ROBOT_PATTERN = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")


@dataclass
class Robot:
    pos: (int, int)
    vel: (int, int)


def read_input():
    filename = "p14.input.txt"
    max_x, max_y = 101, 103
    if "test" in filename:
        max_x, max_y = 11, 7

    robots = []
    with open(filename, "r") as f:
        for line in f.readlines():
            match = ROBOT_PATTERN.match(line)
            x = int(match.group(1))
            y = int(match.group(2))
            dx = int(match.group(3))
            dy = int(match.group(4))

            robots.append(Robot((x, y), (dx, dy)))

    return robots, max_x, max_y


def update_robot(robot: Robot, max_x: int, max_y: int) -> None:
    posx, posy = robot.pos
    velx, vely = robot.vel
    newx, newy = posx + velx, posy + vely
    if newx >= max_x:
        newx = newx - max_x
    if newx < 0:
        newx = newx + max_x
    if newy >= max_y:
        newy = newy - max_y
    if newy < 0:
        newy = newy + max_y
    robot.pos = (newx, newy)


def print_grid(robots: [Robot], max_x, max_y, f) -> None:
    grid = []
    for iy in range(max_y):
        grid.append([])
        for ix in range(max_x):
            grid[iy].append(0)

    for robot in robots:
        y, x = robot.pos[1], robot.pos[0]
        grid[y][x] += 1
    for line in grid:
        for i in line:
            if i == 0:
                print(".", end="", file=f)
            else:
                print("X", end="", file=f)
        print(file=f)


def incomplete_flood(robots: [Robot], max_x: int, max_y: int) -> int:
    seen = {(robot.pos[0], robot.pos[1]) for robot in robots}
    max_seen = max_x * max_y

    def find_starts():
        starts = []
        for y in range(max_y):
            for x in range(max_x):
                if (x, y) in seen:
                    continue
                starts.append((x, y))
                if len(starts) > 2:
                    return starts

    starts = find_starts()

    for start in starts:
        stack = [start]
        while len(stack) > 0:
            x, y = stack.pop()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < max_x and 0 <= ny < max_y:
                    stack.append((nx, ny))
    diff = max_seen - len(seen)
    return diff if 10 < diff < (max_seen - len(robots)) else 0


def check_tree(robots: [Robot], max_x: int, max_y: int, outfile: Path) -> None:
    diff = incomplete_flood(robots, max_x, max_y)
    if diff > 0:
        with open(outfile, "w") as f:
            print_grid(robots, max_x, max_y, f)
        input(
            f"{str(f.name)} might be a tree ({diff}).  Press Enter to continue looking or Ctrl+C to quit."
        )


if __name__ == "__main__":
    robots, max_x, max_y = read_input()
    this_file = Path(__file__)
    out_dir = this_file.parent / "p14.out"
    out_dir.mkdir(exist_ok=True)
    for i in range(1, 101):
        for robot in robots:
            update_robot(robot, max_x, max_y)
        check_tree(robots, max_x, max_y, out_dir / f"{i}.txt")
    mid_x = max_x // 2
    mid_y = max_y // 2
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        x, y = robot.pos
        if x == mid_x or y == mid_y:
            continue
        if 0 <= x < mid_x:
            if 0 <= y < mid_y:
                quadrants[0] += 1
            else:
                quadrants[1] += 1
        else:
            if 0 <= y < mid_y:
                quadrants[2] += 1
            else:
                quadrants[3] += 1

    print(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])
    for i in range(101, 100000):
        for robot in robots:
            update_robot(robot, max_x, max_y)
        check_tree(robots, max_x, max_y, out_dir / f"{i}.txt")
