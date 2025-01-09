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
                program = [int(i) for i in m.group(1).split(",")]
    return registers, program


def process_one(registers, program, ip) -> (int, Optional[int]):
    def combo_value(operand):
        if operand <= 3:
            return operand
        if operand == 7:
            assert False
        return registers[operand - 4]

    opcode = program[ip]
    operand = program[ip + 1]
    if opcode == 0:
        result = registers[0] // 2 ** combo_value(operand)
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
        result = registers[0] // 2 ** combo_value(operand)
        registers[1] = result
        return ip + 2, None
    elif opcode == 7:
        result = registers[0] // 2 ** combo_value(operand)
        registers[2] = result
        return ip + 2, None
    else:
        assert False


def run(registers, program):
    working_registers = registers[:]
    ip = 0
    output_arr = []
    while ip < len(program):
        ip, output = process_one(working_registers, program, ip)
        if output is not None:
            output_arr.append(output)
    return output_arr


def print_output(output_arr):
    print(",".join([str(i) for i in output_arr]))


if __name__ == "__main__":
    registers, program = read_input()
    output_arr = run(registers, program)
    print_output(output_arr)
    """
    Program:

    2,4: B = A % 8
    1,1: B = B ^ 1
    7,5: C = A // 2**B
    1,5: B = B ^ 5
    4,2: B = B ^ C
    5,5: output.append(B % 8)
    0,3: A = A // (2**3)
    3,0: If A > 0 loop to 2,4

    - This appears to be looking at each octet in sequence from least sig to most
    - Start with trying to match -1st program octet and then add more sig octets to A
    """

    def search(A, i):
        for a in range(0, 8):
            A_tmp = A + a
            output_arr = run([A_tmp, 0, 0], program)
            if output_arr == program:
                return A_tmp
            if output_arr == program[-len(output_arr) :]:
                r = search(A_tmp * 8, i + 1)
                if r:
                    return r
        return None

    A = 0
    print(search(A, 0))
