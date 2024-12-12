def inputs():
    with open("p7.input.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            total_str, rest = line.split(": ")
            yield int(total_str), [int(i) for i in rest.split(" ")]


def can_compute(total, nums):
    firstnum = nums[0]
    if firstnum > total:
        return False
    if len(nums) == 1:
        return firstnum == total

    numsadd = nums[1:]
    numsadd[0] += firstnum
    numsmult = nums[1:]
    numsmult[0] *= firstnum
    can_add = can_compute(total, numsadd)
    if can_add:
        return True
    return can_compute(total, numsmult)



if __name__ == "__main__":
    total_totals = 0
    for total, nums in inputs():
        if can_compute(total, nums):
            total_totals += total

    print(total_totals)