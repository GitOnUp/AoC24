import heapq
from dataclasses import dataclass

WALL = "#"
EMPTY = "."
START = "S"
END = "E"

# In rotation order
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


@dataclass
class State:
    direction_id: int
    score: int
    location: (int, int)

    def __lt__(self, other):
        return self.score < other.score

    def __hash__(self):
        return hash((self.direction_id, self.score, self.location))

    def __eq__(self, other):
        return self.direction_id == other.direction_id and self.score == other.score and self.location == other.location

    def tuple_for_seen(self):
        return (self.direction_id, self.location[0], self.location[1])

    def direction(self):
        return DIRECTIONS[self.direction_id]

    def as_rotate_cw(self):
        dir_id = self.direction_id + 1
        if dir_id == len(DIRECTIONS):
            dir_id = 0
        return State(dir_id, self.score+1000, self.location)

    def as_rotate_ccw(self):
        dir_id = self.direction_id - 1
        if dir_id < 0:
            dir_id = len(DIRECTIONS) - 1
        return State(dir_id, self.score+1000, self.location)

    def as_move(self):
        x, y = self.location
        dx, dy = DIRECTIONS[self.direction_id]
        return State(self.direction_id, self.score+1, (x + dx, y + dy))


def read_input():
    maze = []
    start = None
    end = None
    with open("p16.input.txt", "r") as f:
        for y, line in enumerate(f.readlines()):
            maze_line = []
            line = line.strip()
            for x, c in enumerate(line):
                maze_line.append(c)
                if c == START:
                    start = (x, y)
                elif c == END:
                    end = (x, y)
            maze.append(maze_line)
    return maze, start, end


def find_lowest_score(maze, start, end):
    heap = [State(0, 0, start)]
    seen = set()
    while len(heap):
        state = heapq.heappop(heap)
        x, y = state.location
        if (x, y) == end:
            return state.score
        if maze[y][x] == WALL:
            continue
        if state.tuple_for_seen() in seen:
            continue
        seen.add(state.tuple_for_seen())
        heapq.heappush(heap, state.as_rotate_cw())
        heapq.heappush(heap, state.as_rotate_ccw())
        heapq.heappush(heap, state.as_move())
    assert False


if __name__ == "__main__":
    maze, start, end = read_input()
    print(find_lowest_score(maze, start, end))

# 104504 is too high