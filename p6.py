DIRECTIONS = [x for x in "<^>v"]

DIRECTION_D = {
    "<": (-1, 0),
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
}


def next_direction(d: (int, int)) -> (int, int):
    if d == (-1, 0):
        return 0, -1
    if d == (0, -1):
        return 1, 0
    if d == (1, 0):
        return 0, 1
    return -1, 0


def read_grid():
    grid = []
    start = None
    with open('p6.input.txt', 'r') as f:
        for y, line in enumerate(f.readlines()):
            grid_line = []
            for x, c in enumerate(line):
                if c in DIRECTIONS:
                    start = (x, y)
                grid_line.append(c)
            grid.append(grid_line)
    return grid, start


def traverse(grid, start):


