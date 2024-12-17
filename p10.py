def read_input():
    topography = []
    with open("p10.input.txt") as f:
        for line in f.readlines():
            line = line.strip()
            topography.append([int(c) for c in line])

    return topography


def at(topography, x, y):
    if x < 0 or y < 0 or y >= len(topography) or x >= len(topography[y]):
        return None
    return topography[y][x]


def trailhead_reachable(topography, height_start, x, y):
    if at(topography, x, y) != height_start:
        return set()
    if height_start == 9:
        return {(x, y)}

    height_start += 1
    rval = set()
    rval |= trailhead_reachable(topography, height_start, x+1, y)
    rval |= trailhead_reachable(topography, height_start, x, y+1)
    rval |= trailhead_reachable(topography, height_start, x-1, y)
    rval |= trailhead_reachable(topography, height_start, x, y-1)
    return rval


if __name__ == "__main__":
    topography = read_input()
    score = 0
    for y in range(len(topography)):
        for x in range(len(topography[y])):
            score += len(trailhead_reachable(topography, 0, x, y))

    print(score)