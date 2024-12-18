from collections import defaultdict, deque


def read_input():
    with open("p11.test.input.txt") as f:
        return [int(s) for s in f.readline().strip().split(" ")]


def build_cache(nblinks):
    cache = defaultdict(list)
    for i in range(100):
        stones = [i]
        cache[i].append(len(stones))
        for ixblink in range(1, nblinks + 1):
            stones = do_blink(stones)
            cache[i].append(len(stones))
    return cache


def do_blinks(stones, nblinks):
    ds = deque(stones)
    total = 0
    while len(stones):
        working_stones = [(stones[0], 0)]
        for i in range(nblinks):
            if stones[0] in cache:
                total += cache[stones[0]][nblinks - i]
            stones = do_blink(stones)
    return stones


def do_blink(stones):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        else:
            dstr = str(stone)
            l = len(dstr)
            if l % 2 == 0:
                new_stones.append(int(dstr[:l//2]))
                new_stones.append(int(dstr[l//2:]))
            else:
                new_stones.append(stone * 2024)

    return new_stones


if __name__ == "__main__":
    stones = read_input()
    cache = build_cache(25)
    stones = do_blinks([(stone, 0) for stone in stones], 25)
    print(len(stones))
