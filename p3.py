import re

MATCHER = re.compile(r'mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))')

if __name__ == "__main__":
    sum = 0
    enabled_sum = 0
    enabled = True
    with open('p3.input.txt') as f:
        instructions = f.read()
        matches = MATCHER.findall(instructions)
        for match in matches:
            n1, n2, do, dont = match
            if do:
                enabled = True
                continue
            if dont:
                enabled = False
                continue
            n1 = int(n1)
            n2 = int(n2)
            if 0 < n1 < 1000 and 0 < n2 < 1000:
                sum += n1 * n2
                if enabled:
                    enabled_sum += n1 * n2
    print(sum, enabled_sum, sep="\n")