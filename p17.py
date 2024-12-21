import re

REGISTER_PATTERN = re.compile(r"Register [ABC]: (\d+)")
PROGRAM_PATTERN = re.compile(r"Program: (.*)")

def read_input():
    registers = []
    program = None
    with open("p17.test.input.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            m = REGISTER_PATTERN.match(line)
            if m:
                registers.append(int(m.group(1)))
                continue
            m = PROGRAM_PATTERN.match(line)
            if m:
                program = [int(i) for i in m.group(1).split(',')]
    return registers, program


def run(registers, program):
    ip = 0

    def combo_value(operand):
        if operand <= 3:
            return operand
        if operand == 7:
            assert False
        return registers[operand - 4]

    while ip < len(program) - 1:
        opcode = program[ip]
        operand = program[ip+1]
        if opcode == 0:
            result = registers[0] // 2**combo_value(operand)
            registers[0] = result
            ip += 2
        elif opcode == 1:
            result = registers[1] ^ operand
            registers[1] = result
            ip += 2
        elif opcode == 2:
        elif opcode == 3:
        elif opcode == 4:
        elif opcode == 5:
        elif opcode == 6:
        elif opcode == 7:
        else:
            assert False

if __name__ == "__main__":
    print(read_input())