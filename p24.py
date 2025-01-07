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


def find_dependencies(circuit, key: str) -> {str}:
    val = circuit[key]
    if isinstance(val, int):
        return set()
    return set(val.wires) | find_dependencies(circuit, val.wires[0]) | find_dependencies(circuit, val.wires[1])


def find_dependent_calcs(circuit, wire: str) -> [(Calc, str)]:
    for k, v in list(circuit.items()):
        if not isinstance(v, Calc):
            continue
        if wire in v.wires:
            yield v, k



HALF_ADD_PRE = "HA_"
HALF_ADD_CARRY_PRE = "HAC_"
FULL_ADD_CARRY_PRE = "FAC_"
ADD_WITH_CARRY_PRE = "z"
CARRY_PRE = "C_"


def find_exact_inputs(circuit, wires) -> [(str, Calc)]:
    results = []
    for outwire, val in circuit.items():
        if not isinstance(val, Calc):
            continue
        if set(wires) == set(val.wires):
            results.append((outwire, val))
    return results


def find_exact(circuit, wires, op) -> (str, Calc):
    results = find_exact_inputs(circuit, wires)
    for outwire, calc in results:
        if calc.op == op:
            return outwire, calc
    assert False


def traverse_gates(circuit):
    name_map = {}

    def replace_wire_name(old_name: str, new_name: str):
        items = list(circuit.items())
        for outwire, val in items:
            if outwire == old_name:
                del circuit[old_name]
                circuit[new_name] = val
                continue
            if not isinstance(val, Calc):
                continue
            wires = list(val.wires)
            if old_name not in wires:
                continue
            wires.remove(old_name)
            wires.append(new_name)
            circuit[old_name] = Calc(wires, val.op)
            name_map[new_name] = old_name

    # start with x00, y00 and make the carry
    outwire, calc = find_exact(circuit, ["x00", "y00"], "AND")
    replace_wire_name(outwire, f"{CARRY_PRE}00")

    # then make half adds and half add carries for individual bits
    # if exact match isn't found, find whichever one is there and then swap the other with the wire shared with it
    # TODO how to know which one is right?
    ixbit = 1
    while f"x{str(ixbit).zfill(2)}" in circuit:
        prev_suffix = str(ixbit-1).zfill(2)
        suffix = str(ixbit).zfill(2)
        results = find_exact_inputs(circuit, [f"{c}{suffix}" for c in "xy"])
        # Make half add carry and half add digit
        for outwire, calc in results:
            if calc.op == "AND":
                replace_wire_name(outwire, f"{HALF_ADD_CARRY_PRE}{suffix}")
            else:
                assert calc.op == "XOR"
                replace_wire_name(outwire, f"{HALF_ADD_PRE}{suffix}")

        # use previous carry and make this carry
        outwire, calc = find_exact(circuit, [f"{HALF_ADD_PRE}{suffix}", f"{CARRY_PRE}{prev_suffix}"], "AND")

        ixbit += 1


if __name__ == "__main__":
    circuit = read_input()
    x = get_wire_nums(circuit, "x")
    y = get_wire_nums(circuit, "y")
    expected = x + y
    print(expected)
    z = get_wire_nums(circuit, "z")
    print(z)

    traverse_gates(circuit)

    # These need to be full adders:
    # https://en.wikipedia.org/wiki/Adder_(electronics)#/media/File:Fulladder.gif
    # for z00, S is the XOR of x00, y00, then cOut is x00 and y00

    for dep in find_dependencies(circuit, "z01"):
        print()
        for calc, wire in find_dependent_calcs(circuit, dep):
            print(calc, wire)