DIRS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


class Puzzle:
    def __init__(self):
        with open("p4.input.txt", "r") as raw:
            self.lines = [list(line.strip()) for line in raw.readlines()]

    def at(self, x: int, y: int) -> str:
        if y < 0 or y >= len(self.lines) or x < 0 or x >= len(self.lines[y]):
            return ""
        return self.lines[y][x]

    def find_count_at(self, x: int, y: int, word: str) -> int:
        if self.at(x, y) != word[0]:
            return 0

        count = 0
        for direction in DIRS:
            for i in range(1, len(word)):
                vx, vy = direction[0] * i, direction[1] * i
                if self.at(x + vx, y + vy) != word[i]:
                    break
            else:
                count += 1
        return count

    def find_xmas_count(self) -> int:
        count = 0
        for y in range(len(self.lines)):
            for x in range(len(self.lines[y])):
                count += self.find_count_at(x, y, "XMAS")
        return count

    def find_x_mas_count(self) -> int:
        count = 0
        for y in range(len(self.lines)):
            for x in range(len(self.lines[y])):
                if self.at(x, y) != "A":
                    continue
                d1 = f"{self.at(x-1, y-1)}{self.at(x+1, y+1)}"
                d2 = f"{self.at(x-1, y+1)}{self.at(x+1, y-1)}"
                if d1 not in ["MS", "SM"] or d2 not in ["MS", "SM"]:
                    continue
                count += 1
        return count


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.find_xmas_count())
    print(puzzle.find_x_mas_count())
