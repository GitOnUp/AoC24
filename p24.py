from collections import namedtuple

Calc = namedtuple("Calc", ["wires", "op"])


def read_input():
    circuit = {}
    with open("p24.input.txt", "r") as f:
        doing_wires = True
        for line in f.readlines():
            line = line.strip()
            if not line:
                doing_wires = False
                continue
            if doing_wires:
                wire, val = line.split(": ")
                val = int(val)
                circuit[wire] = val
                continue
            wire1, op, wire2, _, outwire = line.split(" ")
            circuit[outwire] = Calc([wire1, wire2], op)
    return circuit


def find_value(circuit, key):
    val = circuit[key]
    if isinstance(val, int):
        return val
    lval = find_value(circuit, val.wires[0])
    rval = find_value(circuit, val.wires[1])
    if val.op == "AND":
        return lval & rval
    elif val.op == "XOR":
        return lval ^ rval
    else:
        return lval | rval


def get_wire_nums(circuit, prefix: str) -> int:
    total = 0
    keys = list(sorted(filter(lambda key: key[0] == prefix, circuit.keys())))
    for i, k in enumerate(keys):
        total += find_value(circuit, k) * 2**i
    return total


if __name__ == "__main__":
    circuit = read_input()
    x = get_wire_nums(circuit, "x")
    y = get_wire_nums(circuit, "y")
    expected = x + y
    print(x+y)
    z = get_wire_nums(circuit, "z")
    print(z)
    print("{0:b}".format(expected ^ z))
