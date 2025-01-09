def inputs():
    with open("p7.input.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            total_str, rest = line.split(": ")
            yield int(total_str), [int(i) for i in rest.split(" ")]


def can_compute(total, nums, with_concat=False):
    firstnum = nums[0]
    if firstnum > total:
        return False
    if len(nums) == 1:
        return firstnum == total

    numsadd = nums[1:]
    numsadd[0] += firstnum
    numsmult = nums[1:]
    numsmult[0] *= firstnum
    can_add = can_compute(total, numsadd, with_concat)
    if can_add:
        return True
    can_mult = can_compute(total, numsmult, with_concat)
    if can_mult:
        return True
    if with_concat:
        nums_concat = nums[1:]
        nums_concat[0] = int(f"{firstnum}{nums_concat[0]}")
        can_concat = can_compute(total, nums_concat, with_concat)
        if can_concat:
            return True
    return False


if __name__ == "__main__":
    total_totals = 0
    with_concat = 0
    for total, nums in inputs():
        if can_compute(total, nums):
            total_totals += total
            with_concat += total
        elif can_compute(total, nums, with_concat=True):
            with_concat += total

    print(total_totals, with_concat, sep="\n")
