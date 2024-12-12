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


def at(grid, x, y):
    if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[0]):
        return None
    return grid[y][x]


def traverse(grid, start):
    count = 0
    x, y = start
    d = DIRECTION_D[grid[y][x]]
    while True:
        if grid[y][x] != "X":
            count += 1
        grid[y][x] = "X"
        for _ in range(len(DIRECTION_D)):
            dx, dy = d
            next_char = at(grid, x + dx, y + dy)
            if next_char is None:
                return count
            if next_char != "#":
                break
            d = next_direction(d)
        else:
            return count
        x += dx
        y += dy
    return count

if __name__ == '__main__':
    grid, start = read_grid()
    print(traverse(grid, start))