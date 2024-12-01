import re
from collections import defaultdict

INPUT_LINE_MATCHER = re.compile(r"(\d+)\s+(\d+)")


def get_inputs():
    l_arr = []
    r_arr = []
    for line in open('p1.input.txt', 'r').readlines():
        parsed = INPUT_LINE_MATCHER.match(line.strip())
        l, r = parsed.groups(0)
        l_arr.append(int(l))
        r_arr.append(int(r))
    return sorted(l_arr), sorted(r_arr)


l_array, r_array = get_inputs()


def run():
    tot_d = 0
    for l, r in zip(l_array, r_array):
        d = abs(l - r)
        tot_d += d
    return tot_d


def run2():
    freq = defaultdict(int)
    score = 0
    for i in r_array:
        freq[i] += 1
    for j in l_array:
        score += j * freq.get(j, 0)
    return score


if __name__ == "__main__":
    print(run())
    print(run2())
