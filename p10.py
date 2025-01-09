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
        return set(), 0
    if height_start == 9:
        return {(x, y)}, 1

    height_start += 1
    rval = set()
    rating = 0
    for newx, newy in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        reached, subrating = trailhead_reachable(topography, height_start, newx, newy)
        rval |= reached
        rating += subrating
    return rval, rating


if __name__ == "__main__":
    topography = read_input()
    score = 0
    rating = 0
    for y in range(len(topography)):
        for x in range(len(topography[y])):
            reachable, subrating = trailhead_reachable(topography, 0, x, y)
            score += len(reachable)
            rating += subrating

    print(score)
    print(rating)
