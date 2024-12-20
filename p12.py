from collections import defaultdict


def read_plots():
    with open("p12.input.txt", "r") as f:
        plots = [[c for c in line.strip()] for line in f.read().splitlines()]
    return plots


def at(plots, x, y):
    if x < 0 or y < 0 or y >= len(plots) or x >= len(plots[y]):
        return None
    return plots[y][x]


SIDE_MAP = {
    (0, 1): "u",
    (0, -1): "d",
    (1, 0): "l",
    (-1, 0): "r"
}


def flood_fill(plots, x, y):
    char = at(plots, x, y)
    seen = set()
    stack = [(x, y)]
    perimeter = 0
    side_coords = defaultdict(set)
    while len(stack):
        x, y = stack.pop()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        next_coords = []
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newx, newy = x + direction[0], y + direction[1]
            if at(plots, newx, newy) == char:
                next_coords.append((newx, newy))
            else:
                side_coords[(newx, newy)].add(SIDE_MAP[direction])
        perimeter += 4 - len(next_coords)
        stack.extend(next_coords)

    sides = 0
    while len(side_coords) > 0:
        x, y = next(iter(side_coords))
        if len(side_coords[(x, y)]) == 0:
            del side_coords[(x, y)]
            continue
        side_dir = side_coords[(x, y)].pop()
        sides += 1
        if side_dir in ["r", "l"]:
            directions = [(0, -1), (0, 1)]
        else:
            directions = [(-1, 0), (1, 0)]

        for direction in directions:
            newx, newy = x + direction[0], y + direction[1]
            while (newx, newy) in side_coords and side_dir in side_coords[(newx, newy)]:
                side_coords[(newx, newy)].remove(side_dir)
                if side_coords[(newx, newy)] == 0:
                    del side_coords[(newx, newy)]
                newx, newy = newx + direction[0], newy + direction[1]

    return len(seen), perimeter, seen, sides


if __name__ == "__main__":
    plots = read_plots()
    seen = set()
    total = 0
    sides_total = 0
    for y in range(len(plots)):
        for x in range(len(plots[y])):
            if (x, y) in seen:
                continue
            sub_area, sub_perimeter, sub_seen, sub_sides = flood_fill(plots, x, y)
            total += sub_area * sub_perimeter
            sides_total += sub_area * sub_sides
            seen |= sub_seen
    print(total)
    print(sides_total)