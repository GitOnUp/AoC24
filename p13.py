import re
from dataclasses import dataclass

BUTTON_PATTERN = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
PRIZE_PATTERN = re.compile(r"Prize: X=(\d+), Y=(\d+)")


@dataclass
class Machine:
    a: (int, int)
    b: (int, int)
    prize: (int, int)

    @classmethod
    def parse(cls, lines):
        a_match = BUTTON_PATTERN.match(lines[0])
        a = (int(a_match.group(1)), int(a_match.group(2)))
        b_match = BUTTON_PATTERN.match(lines[1])
        b = (int(b_match.group(1)), int(b_match.group(2)))
        prize_match = PRIZE_PATTERN.match(lines[2])
        prize = (int(prize_match.group(1)), int(prize_match.group(2)))
        return cls(a, b, prize)


def read_input() -> [Machine]:
    with open("p13.input.txt", "r") as f:
        lines = list(
            filter(lambda line: line, [line.strip() for line in f.readlines()])
        )

    machines = []
    for i in range(0, len(lines), 3):
        machines.append(Machine.parse(lines[i : i + 3]))

    return machines


def play_machine(machine: Machine) -> int:
    b = machine.b[0] * machine.prize[1] - machine.b[1] * machine.prize[0]
    m = machine.b[0] * machine.a[1] - machine.b[1] * machine.a[0]

    if b % m != 0:
        return 0
    a = b // m
    ax = a * machine.a[0]
    dx = machine.prize[0] - ax
    if dx % machine.b[0] != 0:
        return 0
    b = dx // machine.b[0]
    return (a * 3) + b


if __name__ == "__main__":
    machines = read_input()
    total = 0
    for machine in machines:
        total += play_machine(machine)
    print(total)
    total = 0
    for machine in machines:
        machine.prize = (
            machine.prize[0] + 10000000000000,
            machine.prize[1] + 10000000000000,
        )
        total += play_machine(machine)
    print(total)
