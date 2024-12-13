
def pack(blocks):
    ix = 0
    reversed_ix_ix = 0
    reversed_indexes = list(reversed(blocks.keys()))
    while reversed_indexes[reversed_ix_ix] > ix:
        if blocks.get(ix) is not None:
            ix += 1
            continue
        next_reversed = reversed_indexes[reversed_ix_ix]
        id = blocks[next_reversed]
        blocks[ix] = id
        del[blocks[next_reversed]]
        reversed_ix_ix += 1
        ix += 1


def checksum(packed):
    checksum = 0
    for i in range(len(packed)):
        checksum += packed[i] * i
    return checksum


if __name__ == "__main__":
    with open("p9.input.txt") as f:
        ftab = f.readline().strip()
    blocks = {}
    current_index = 0
    current_id = 0
    for i, c in enumerate(ftab):
        if i % 2 == 0:
            for ix in range(int(c)):
                blocks[current_index] = current_id
                current_index += 1
            current_id += 1
        else:
            current_index += int(c)

    pack(blocks)
    print(checksum(blocks))