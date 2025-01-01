from typing import Optional, Tuple


def read_input():
    with open("p21.input.txt", "r") as f:
        return [l.strip() for l in f.readlines()]


BLANK = ""
ACTIVATE = "A"

KEYPAD_LOCS = {
    "7": (0, 0), "8": (1, 0), "9": (2, 0),
    "4": (0, 1), "5": (1, 1), "6": (2, 1),
    "1": (0, 2), "2": (1, 2), "3": (2, 2),
    "": (0, 3), "0": (1, 3), "A": (2, 3),
}

DPAD_LOCS = {
    "": (0, 0), "^": (1, 0), "A": (2, 0),
    "<": (0, 1), "v": (1, 1), ">": (2, 1)
}


def _path(is_keypad: bool, char: str, x: int, y: int, press: bool) -> [str]:
    coord_map = KEYPAD_LOCS if is_keypad else DPAD_LOCS
    blankx, blanky = coord_map[BLANK]
    nx, ny = coord_map[char]
    dx, dy = nx - x, ny - y
    x_path = "<" * -dx if dx < 0 else ">" * dx
    y_path = "^" * -dy if dy < 0 else "v" * dy
    x_first = x_path + y_path
    y_first = y_path + x_path
    if press:
        x_first += "A"
        y_first += "A"
    if x == blankx and ny == blanky:
        return [x_first]
    elif y == blanky and nx == blankx:
        return [y_first]
    elif x_first == y_first:
        return [x_first]
    else:
        return [x_first, y_first]


class Keypad:
    def __init__(self, xy: Optional[Tuple[int, int]] = None):
        if xy is None:
            self.x = 2
            self.y = 3
        else:
            self.x, self.y = xy

    def paths_to(self, char: str, press: bool = True) -> [str]:
        return _path(True, char, self.x, self.y, press)

    @classmethod
    def move_to(cls, char: str) -> "Keypad":
        return cls(KEYPAD_LOCS[char])


class Dpad:
    def __init__(self, xy: Optional[Tuple[int, int]] = None):
        if xy is None:
            self.x = 2
            self.y = 0
        else:
            self.x, self.y = xy

    def paths_to(self, char: str, press: bool = True) -> [str]:
        return _path(False, char, self.x, self.y, press)

    @classmethod
    def move_to(cls, char: str) -> "Dpad":
        return cls(DPAD_LOCS[char])


def find_paths(pad: Dpad | Keypad, seq: str) -> [str]:
    paths = pad.paths_to(seq[0])
    pad = pad.move_to(seq[0])
    for c in seq[1:]:
        new_paths = []
        for path in paths:
            new_subpaths = pad.paths_to(c)
            for new_subpath in new_subpaths:
                new_paths.append(path + new_subpath)
        paths = new_paths
        pad = pad.move_to(c)
    return paths


def search_complexities(pad_types: [type], seq: str) -> int:
    init_paths = find_paths(pad_types[0](), seq)
    current = list(zip(init_paths, [1] * len(init_paths)))
    cost = None
    while current:
        path, pad_type_ix = current.pop()
        if pad_type_ix == len(pad_types):
            if cost is None or cost > len(path):
                cost = len(path)
            continue
        next_paths = find_paths(pad_types[pad_type_ix](), path)
        for p in next_paths:
            current.append((p, pad_type_ix + 1))
    return cost * int(seq[:-1])


if __name__ == "__main__":
    k = Keypad()
    sequences = read_input()
    total = 0
    first_types = [Keypad, Dpad, Dpad]
    for s in sequences:
        total += search_complexities(first_types, s)
    print(total)
    second_types = [Keypad] + [Dpad] * 25
    total = 0
    for s in sequences:
        total += search_complexities(second_types, s)
    print(total)