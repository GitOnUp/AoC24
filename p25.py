def read_input():
    locks = []
    keys = []
    with open("p25.input.txt", "r") as f:
        def process_lock(lock):
            depths = [0] * len(lock[0])
            for line in lock[1:len(lock)-1]:
                for i, c in enumerate(line):
                    if c == "#":
                        depths[i] += 1
            locks.append(depths)

        def process_key(key):
            heights = [5] * len(key[0])
            for line in key[1:len(key)-1]:
                for i, c in enumerate(line):
                    if c == ".":
                        heights[i] -= 1
            keys.append(heights)

        while True:
            block = [f.readline().strip() for _ in range(7)]
            if block[0] == "":
                break
            if block[0][0] == "#":
                process_lock(block)
            else:
                process_key(block)
            if f.readline() == "":
                break

    return locks, keys


def find_fit(locks, keys):
    matches = 0
    for lock in locks:
        for key in keys:
            for i in range(len(key)):
                if key[i] + lock[i] > 5:
                    break
            else:
                matches += 1
    return matches


if __name__ == "__main__":
    locks, keys = read_input()
    print(find_fit(locks, keys))