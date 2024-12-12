from collections import defaultdict

DIRECTIONS = [x for x in "<^>v"]

DIRECTION_D = {
    "<": (-1, 0),
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
}

D_DIRECTION = {v: k for k, v in DIRECTION_D.items()}

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
            for x, c in enumerate(line.strip()):
                if c in DIRECTIONS:
                    start = (x, y)
                grid_line.append(c)
            grid.append(grid_line)
    return grid, start


def at(grid, x, y):
    if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[0]):
        return None
    return grid[y][x]


class LoopDetected(Exception):
    pass


def traverse(grid, start):
    seen = defaultdict(set)
    count = 0
    x, y = start
    d = DIRECTION_D[grid[y][x]]
    dc = D_DIRECTION[d]
    while True:
        if (x, y) not in seen:
            count += 1
        elif dc in seen[(x, y)]:
            return -1, seen
        seen[(x, y)].add(dc)
        for _ in range(len(DIRECTION_D)):
            dx, dy = d
            next_char = at(grid, x + dx, y + dy)
            if next_char is None:
                return count, seen
            if next_char != "#":
                break
            d = next_direction(d)
            dc = D_DIRECTION[d]
        else:
            assert False
        x += dx
        y += dy


if __name__ == '__main__':
    grid, start = read_grid()
    count, seen = traverse(grid, start)
    print(count)
    loops = 0
    for coords in seen.keys():
        x, y = coords
        if (x, y) == start: continue
        grid[y][x] = "#"
        count, _ = traverse(grid, start)
        if count < 0:
            loops += 1
        grid[y][x] = "."
    print(loops)
