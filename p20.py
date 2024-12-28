from typing import Any

WALL = "#"
START = "S"
END = "E"
EMPTY = "."

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def load_input():
    with open("p20.input.txt", "r") as f:
        return Grid(f)


class Grid:
    def __init__(self, f):
        self.grid = []
        self.start = None
        self.end = None
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            gridline = []
            for x, c in enumerate(line):
                if c == START:
                    self.start = (x, y)
                if c == END:
                    self.end = (x, y)
                gridline.append(c)
            self.grid.append(gridline)

    def at(self, x: int, y: int) -> Any:
        if x < 0 or y < 0 or y >= len(self.grid) or x >= len(self.grid[y]):
            return None
        return self.grid[y][x]

    def set(self, x: int, y: int, val: Any) -> None:
        if x < 0 or y < 0 or y >= len(self.grid) or x >= len(self.grid[y]):
            return None
        self.grid[y][x] = val

    def moves_from(self, x: int, y: int) -> (int, int):
        for d in DIRECTIONS:
            dx, dy = d
            nx, ny = dx + x, dy + y
            if nx < 0 or ny < 0 or ny >= len(self.grid) or nx >= len(self.grid[y]):
                continue
            yield nx, ny


def set_distances(grid: Grid) -> [(int, int)]:
    xy = grid.start
    distance = 0
    path = []
    while xy != grid.end:
        path.append(xy)
        grid.set(*xy, distance)
        distance += 1
        for move in grid.moves_from(*xy):
            at_move = grid.at(*move)
            if at_move in (EMPTY, END):
                xy = move
                break
    path.append(xy)
    grid.set(*xy, distance)
    return path


if __name__ == "__main__":
    grid = load_input()
    path = set_distances(grid)
    print(len(path) - 1)

    save_100s = 0
    for locxy in path:
        for direction in DIRECTIONS:
            dx, dy = direction
            mx, my = locxy[0] + dx, locxy[1] + dy
            at_move = grid.at(mx, my)
            if at_move == WALL:
                start_cost = grid.at(*locxy)
                assert isinstance(start_cost, int)
                end_cost = grid.at(mx + dx, my + dy)
                if not isinstance(end_cost, int):
                    continue
                diff = end_cost - start_cost - 2
                if diff <= 0:
                    continue
                if diff >= 100:
                    save_100s += 1
    print(save_100s)


