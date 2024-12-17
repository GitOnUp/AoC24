def read_input():
    with open("p11.input.txt") as f:
        return [int(s) for s in f.readline().strip().split(" ")]


if __name__ == "__main__":
    stones = read_input()
    for iteration in range(25):
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

        stones = new_stones
    print(len(stones))
