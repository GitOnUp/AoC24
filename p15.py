DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
DIRECTION_CHARS = "v^><"

DIRECTION_MAP = {k: v for (k, v) in zip(DIRECTION_CHARS, DIRECTIONS)}

WALL = "#"
BOX = "O"
ROBOT = "@"
EMPTY = "."


def read_input():
    robot_coord = None
    grid_y = 0
    grid = []
    moves = []
    doing_grid = True
    with open("p15.input.txt", "r") as f:
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


def sum_gps(grid):
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == BOX:
                total += (y * 100) + x
    return total


if __name__ == "__main__":
    grid, moves, robot_coord = read_input()
    for move in moves:
        robot_coord = attempt_move(grid, robot_coord, move)
    print(sum_gps(grid))