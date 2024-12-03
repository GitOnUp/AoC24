def read_input():
    ret = []
    with open('p2.input.txt') as f:
        lines = f.readlines()
        for line in lines:
            vals = [int(s) for s in line.strip().split(' ')]
            ret.append(vals)
    return ret


vals = read_input()


def is_safe(report):
    lastdiff = None
    for ix in range(len(report) - 1):
        l, r = report[ix], report[ix + 1]
        diff = l - r
        if not (0 < abs(diff) <= 3):
            return False
        if lastdiff is None:
            lastdiff = diff
            continue
        if (lastdiff < 0 < diff) or (lastdiff > 0 > diff):
            return False
        lastdiff = diff
    return True


def run():
    safes = 0
    fixed_safes = 0
    for report in vals:
        if is_safe(report):
            safes += 1
            continue
        for bad_ix in range(len(report)):
            if is_safe(report[:bad_ix] + report[bad_ix + 1:]):
                fixed_safes += 1
                break
    return safes, safes + fixed_safes


if __name__ == "__main__":
    print(run())
