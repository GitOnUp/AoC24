from collections import defaultdict


def load_grid() -> [str]:
    with open('p8.input.txt') as f:
        return [[c for c in l.strip()] for l in f.readlines()]


def get_positions(grid) -> {str: [(int, int)]}:
    positions = defaultdict(list)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c != ".":
                positions[c].append((x, y))
    return positions


def at(grid, x, y):
    if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[y]):
        return None
    return grid[y][x]


if __name__ == "__main__":
    grid = load_grid()
    positions = get_positions(grid)
    count = 0
    resonant_count = 0
    for c in positions:
        c_positions = positions[c]
        for ixpos, pos in enumerate(c_positions):
            working_position = c_positions[ixpos]
            other_positions = c_positions[:ixpos] + c_positions[ixpos+1:]
            for other_pos in other_positions:
                current_working = working_position
                x, y = current_working
                dx, dy = working_position[0] - other_pos[0], working_position[1] - other_pos[1]
                while True:
                    gp = at(grid, x, y)
                    if gp is None:
                        break
                    if gp != "#":
                        grid[y][x] = "#"
                        resonant_count += 1
                    current_working = (x, y)
                    x, y = current_working[0] + dx, current_working[1] + dy
    print(count, resonant_count)
