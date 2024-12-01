import re

INPUT_LINE_MATCHER = re.compile(r"(\d+)\s+(\d+)")


def get_inputs():
    l_arr = []
    r_arr = []
    for line in open('p1.input.txt', 'r').readlines():
        parsed = INPUT_LINE_MATCHER.match(line.strip())
        l, r = parsed.groups(0)
        l_arr.append(int(l))
        r_arr.append(int(r))
    return l_arr, r_arr


def run():
    l_array, r_array = get_inputs()
    tot_d = 0
    for l, r in zip(sorted(l_array), sorted(r_array)):
        d = abs(l - r)
        tot_d += d
    return tot_d


if __name__ == "__main__":
    print(run())
