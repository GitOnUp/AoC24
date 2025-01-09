from collections import defaultdict, deque


def read_input():
    with open("p11.input.txt") as f:
        return [int(s) for s in f.readline().strip().split(" ")]


def do_blink(stones):
    new_stones = []
    for stone in stones:
        val, mult = stone
        if val == 0:
            new_stones.append((1, mult))
        else:
            dstr = str(val)
            l = len(dstr)
            if l % 2 == 0:
                new_stones.append((int(dstr[: l // 2]), mult))
                new_stones.append((int(dstr[l // 2 :]), mult))
            else:
                new_stones.append((val * 2024, mult))
    counts = defaultdict(int)
    for stone in new_stones:
        counts[stone[0]] += stone[1]
    return list(counts.items())


if __name__ == "__main__":
    for count in [25, 75]:
        stones = [(stone, 1) for stone in read_input()]
        for i in range(count):
            stones = do_blink(stones)
        total = 0
        for stone in stones:
            _, mult = stone
            total += mult
        print(total)
