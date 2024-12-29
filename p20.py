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

    def in_grid(self, x: int, y: int):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y])

    def at(self, x: int, y: int) -> Any:
        if self.in_grid(x, y):
            return self.grid[y][x]
        return None

    def set(self, x: int, y: int, val: Any) -> None:
        if self.in_grid(x, y):
            self.grid[y][x] = val

    def moves_from(self, x: int, y: int) -> (int, int):
        for d in DIRECTIONS:
            dx, dy = d
            nx, ny = dx + x, dy + y
            if self.in_grid(nx, ny):
                yield nx, ny

    def points_distance_from(self, x: int, y: int, dist: int):
        points = set()
        for dx in range(0, dist + 1):
            dy = dist - dx
            for mult in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                mx, my = mult
                px, py = x + (mx * dx), y + (my * dy)
                if self.in_grid(px, py) and (px, py) not in points:
                    yield px, py
                    points.add((px, py))


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

    save_100s_2 = 0
    save_100s_20 = 0
    for locxy in path:
        start_cost = grid.at(*locxy)
        for dist in range(2, 21):
            for (px, py) in grid.points_distance_from(*locxy, dist):
                assert isinstance(start_cost, int)
                end_cost = grid.at(px, py)
                if not isinstance(end_cost, int):
                    continue
                diff = end_cost - start_cost - dist
                if diff <= 0:
                    continue
                if diff >= 100:
                    save_100s_20 += 1
                    if dist == 2:
                        save_100s_2 += 1
    print(save_100s_2)
    print(save_100s_20)

