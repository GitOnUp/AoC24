from collections import deque
from dataclasses import dataclass

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def read_input():
    corruptions = []
    fname = "p18.input.txt"
    dims = (70, 70)
    if "test" in fname:
        dims = (6, 6)
    with open(fname, "r") as f:
        for line in f.readlines():
            line = line.strip()
            x, y = [int(i) for i in line.split(",")]
            corruptions.append((x, y))
    return corruptions, dims


if __name__ == "__main__":
    corruptions, dims = read_input()

    def find(n_corrupt):
        cset = set(corruptions[:n_corrupt])
        seen = set()

        @dataclass
        class State:
            x: int
            y: int
            path: set

            def __lt__(self, other):
                return self.y < other.y and self.x < other.x

            def pos(self):
                return (self.x, self.y)

        search = deque([State(0, 0, set())])
        while len(search) > 0:
            head = search.popleft()
            if head.pos() == dims:
                return len(head.path)
                break
            for d in DIRECTIONS:
                dx, dy = d
                nx, ny = head.x + dx, head.y + dy
                if nx < 0 or ny < 0 or nx > dims[0] or ny > dims[1]:
                    continue
                if (nx, ny) in seen:
                    continue
                if (nx, ny) in cset:
                    continue
                seen.add((nx, ny))
                search.append(State(nx, ny, head.path | {(nx, ny)}))
        return None

    print(find(1024))
    for i in range(1024, len(corruptions)):
        if not find(i):
            print(",".join([str(i) for i in corruptions[i - 1]]))
            break
