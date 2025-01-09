class FileDef:
    id: int
    start: int
    end: int
    size: int

    def __init__(self, id: int, start: int, end: int):
        self.id = id
        self.start = start
        self.end = end
        self.size = end - start

    def __repr__(self):
        return f"{self.id}: {self.start}-{self.end} ({self.size})"


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
        del [blocks[next_reversed]]
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
    files = []  # (ix, len), ix into files is file ID
    gaps = []
    current_index = 0
    current_id = 0
    for i, c in enumerate(ftab):
        if i % 2 == 0:
            file_length = int(c)
            files.append(
                FileDef(current_id, current_index, current_index + file_length)
            )
            for ix in range(file_length):
                blocks[current_index] = current_id
                current_index += 1
            current_id += 1
        else:
            current_index += int(c)

    pack(blocks)
    print(checksum(blocks))

    iback = len(files) - 1
    while iback >= 0:
        last_file = files[iback]
        for i in range(len(files[:iback])):
            gap = files[i + 1].start - files[i].end
            if gap >= last_file.size:
                files = (
                    files[: i + 1]
                    + [last_file]
                    + files[i + 1 : iback]
                    + files[iback + 1 :]
                )
                last_file.start = files[i].end
                last_file.end = last_file.start + last_file.size
                break
        else:
            iback -= 1

    files_checksum = 0
    for file in files:
        for ix in range(file.start, file.end):
            files_checksum += ix * file.id

    print(files_checksum)
