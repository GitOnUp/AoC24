from collections import defaultdict
from functools import cache


def read_input():
    desired = []
    with open("p19.input.txt", "r") as f:
        towels_raw = f.readline().strip()
        towels = [t for t in towels_raw.split(", ")]
        f.readline()
        for l in f.readlines():
            desired.append(l.strip())
    return towels, desired

def solve():
    towels, desired = read_input()
    tmap = defaultdict(list)
    for towel in towels:
        tmap[towel[0]].append(towel)

    @cache
    def count_possible(_remaining):
        if not _remaining:
            return 1
        next_char = _remaining[0]
        total = 0
        for next_pattern in tmap.get(next_char, []):
            if _remaining[:len(next_pattern)] != next_pattern:
                continue
            next_remaining = _remaining[len(next_pattern):]
            total += count_possible(next_remaining)
        return total

    possible = 0
    total = 0
    for d in desired:
        subtotal = count_possible(d)
        total += subtotal
        if subtotal:
            possible += 1

    print(possible)
    print(total)


if __name__ == "__main__":
    solve()