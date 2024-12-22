import re
from typing import Optional

REGISTER_PATTERN = re.compile(r"Register [ABC]: (\d+)")
PROGRAM_PATTERN = re.compile(r"Program: (.*)")

def read_input():
    registers = []
    program = None
    with open("p17.input.txt", "r") as f:
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


def process_one(registers, program, ip) -> (int, Optional[int]):
    def combo_value(operand):
        if operand <= 3:
            return operand
        if operand == 7:
            assert False
        return registers[operand - 4]

    opcode = program[ip]
    operand = program[ip+1]
    if opcode == 0:
        result = registers[0] // 2**combo_value(operand)
        registers[0] = result
        return ip + 2, None
    elif opcode == 1:
        result = registers[1] ^ operand
        registers[1] = result
        return ip + 2, None
    elif opcode == 2:
        result = combo_value(operand) % 8
        registers[1] = result
        return ip + 2, None
    elif opcode == 3:
        if registers[0] != 0:
            return operand, None
        else:
            return ip + 2, None
    elif opcode == 4:
        result = registers[1] ^ registers[2]
        registers[1] = result
        return ip + 2, None
    elif opcode == 5:
        output = combo_value(operand) % 8
        return ip + 2, output
    elif opcode == 6:
        result = registers[0] // 2**combo_value(operand)
        registers[1] = result
        return ip + 2, None
    elif opcode == 7:
        result = registers[0] // 2 ** combo_value(operand)
        registers[2] = result
        return ip + 2, None
    else:
        assert False


if __name__ == "__main__":
    registers, program = read_input()
    ip = 0
    output_arr = []
    working_registers = registers[:]
    while ip < len(program):
        ip, output = process_one(working_registers, program, ip)
        if output is not None:
            output_arr.append(output)
    print(",".join([str(i) for i in output_arr]))

    a = 0
    while True:
        a = int(input("Test A: "))
        ip = 0
        output_arr = []
        working_registers = [a] + registers[1:]
        while ip < len(program):
            ip, output = process_one(working_registers, program, ip)
            if output is not None:
                output_arr.append(output)
        print("Output:  " + ",".join([str(i) for i in output_arr]))
        print("Program: " + ",".join([str(i) for i in program]))
