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
    def is_possible(_desired, _current):
        if _desired == _current:
            return True
        next_char = _desired[len(_current)]
        for next_pattern in tmap.get(next_char, []):
            if _desired[len(_current):len(_current)+len(next_pattern)] == next_pattern and is_possible(_desired, _current + next_pattern):
                return True
        return False

    total = 0
    for d in desired:
        if is_possible(d, ""):
            total += 1

    print(total)

if __name__ == "__main__":
    solve()