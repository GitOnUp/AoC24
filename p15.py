DOWN = (0, 1)
UP = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)
DIRECTIONS = [DOWN, UP, RIGHT, LEFT]
DIRECTION_CHARS = "v^><"

DIRECTION_MAP = {k: v for (k, v) in zip(DIRECTION_CHARS, DIRECTIONS)}

WALL = "#"
BOX = "O"
ROBOT = "@"
EMPTY = "."
BOX_L = "["
BOX_R = "]"


def read_input():
    robot_coord = None
    grid_y = 0
    grid = []
    moves = []
    doing_grid = True
    with open("p15.test.input.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                if doing_grid:
                    doing_grid = False
                else:
                    break
                continue

            if doing_grid:
                grid_line = []
                for x, c in enumerate(line):
                    if c == ROBOT:
                        robot_coord = (x, grid_y)
                    grid_line.append(c)
                grid.append(grid_line)
                grid_y += 1
                continue

            moves.extend([DIRECTION_MAP[c] for c in line])
    return grid, moves, robot_coord


def attempt_move(grid, robot_coord, move):
    dx, dy = move
    x, y = robot_coord
    stack = [(ROBOT, x + dx, y + dy)]
    x, y = x + dx, y + dy
    while True:
        item = grid[y][x]
        if item == WALL:
            return robot_coord
        if item == BOX:
            stack.append((BOX, x + dx, y + dy))
        if item == EMPTY:
            break
        x, y = x + dx, y + dy

    new_robot_coord = None
    while len(stack) > 0:
        item, x, y = stack.pop()
        grid[y][x] = item
        if item == ROBOT:
            new_robot_coord = (x, y)
    grid[robot_coord[1]][robot_coord[0]] = EMPTY
    return new_robot_coord


def expand_grid(grid):
    new_grid = []
    new_robot_coord = None
    for y, row in enumerate(grid):
        new_row = []
        for x, c in enumerate(row):
            if c == WALL:
                new_row.extend([WALL, WALL])
            elif c == BOX:
                new_row.extend([BOX_L, BOX_R])
            elif c == ROBOT:
                new_row.extend([ROBOT, EMPTY])
                new_robot_coord = (2 * x, y)
            else:
                new_row.extend([EMPTY, EMPTY])
        new_grid.append(new_row)
    return new_grid, new_robot_coord


def sum_gps(grid):
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == BOX:
                total += (y * 100) + x
    return total


def sum_gps_wide(grid):
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pass
    return total


if __name__ == "__main__":
    grid, moves, robot_coord = read_input()
    for move in moves:
        robot_coord = attempt_move(grid, robot_coord, move)
    print(sum_gps(grid))

    grid, moves, _ = read_input()
    grid, robot_coord = expand_grid(grid)
    for move in moves:
        robot_coord = attempt_move(grid, robot_coord, move)
    print(sum_gps_wide(grid))
