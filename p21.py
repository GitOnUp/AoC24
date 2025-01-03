import re
from functools import cache
from typing import Union, Tuple


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


@cache
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


class Pad:
    def __init__(self, coords: {str: (int, int)}, start: Union[Tuple[int, int], str]):
        self.coords = coords
        if isinstance(start, str):
            self.x, self.y = self.coords[start]
        else:
            self.x, self.y = start

    def paths_to(self, char: str, press: bool = True) -> [str]:
        return _path(self.coords is KEYPAD_LOCS, char, self.x, self.y, press)

    def move_to(self, char: str) -> None:
        self.x, self.y = self.coords[char]


class Keypad(Pad):
    def __init__(self):
        super().__init__(KEYPAD_LOCS, (2, 3))


class Dpad(Pad):
    def __init__(self):
        super().__init__(DPAD_LOCS, (2, 0))


def find_paths(pad: Pad, seq: str) -> [str]:
    paths = pad.paths_to(seq[0])
    pad.move_to(seq[0])
    for c in seq[1:]:
        new_paths = []
        for path in paths:
            new_subpaths = pad.paths_to(c)
            for new_subpath in new_subpaths:
                new_paths.append(path + new_subpath)
        paths = new_paths
        pad.move_to(c)
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


SPLIT_REGEX = re.compile(r"[v^<>]*A")
find_min_cache = {}  # {subpath: length}


@cache
def find_min(subpath: str, level: int, maxlevel: int) -> int:
    # cached = find_min_cache.get(subpath)
    # if cached:
    #     return cached
    if level == maxlevel:
        return len(subpath)
    elements = SPLIT_REGEX.findall(subpath)
    pad = Dpad()
    total_length = 0
    for element in elements:
        element_paths = find_paths(pad, element)
        total_length += min([find_min(p, level+1, maxlevel) for p in element_paths])
    # find_min_cache[subpath] = total_length
    return total_length


def score_sequence(seq: str, levels: int) -> int:
    kpaths = find_paths(Keypad(), seq)
    return min([find_min(kpath, 0, levels) for kpath in kpaths]) * int(seq[:-1])


if __name__ == "__main__":
    sequences = read_input()
    p1_total = 0
    p2_total = 0
    for s in sequences:
        p1_total += score_sequence(s, 2)
        p2_total += score_sequence(s, 25)
    print(p1_total)
    print(p2_total)
