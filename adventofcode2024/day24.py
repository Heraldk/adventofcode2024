from dataclasses import dataclass, field
from enum import StrEnum, auto

from common import AdventSolution


class Op(StrEnum):
    AND = auto()
    OR = auto()
    XOR = auto()


@dataclass
class Gate:
    op: Op
    input1: str
    input2: str
    output: str


def parse_input(lines: list[str]) -> tuple[dict[str, int], dict[str, Gate]]:
    inputs = {}
    gates = {}
    for line in lines:
        if line.strip() == "":
            continue
        vals = line.strip().split(":")
        if len(vals) > 1:
            inputs[vals[0]] = int(vals[1].strip())
        else:
            arrow = line.find("->")
            left_side = line[0:arrow].strip().split(" ")
            right_side = line[arrow + 2 :].strip()
            match left_side[1]:
                case "AND":
                    op = Op.AND
                case "XOR":
                    op = Op.XOR
                case "OR":
                    op = Op.OR
            gates[right_side] = Gate(op, left_side[0], left_side[2], right_side)
    return inputs, gates


def determine_values(inputs: dict[str, int], gates: dict[str, Gate]) -> dict[str, int]:
    gates_to_process = {gate: False for gate in gates.keys()}
    outputs = {k: v for k, v in inputs.items()}
    done = False
    while not done:
        done = True
        for o, gate in gates.items():
            if gates_to_process[o]:
                continue
            if gate.input1 not in outputs or gate.input2 not in outputs:
                continue
            done = False
            gates_to_process[gate.output] = True
            match gate.op:
                case Op.AND:
                    output = outputs[gate.input1] & outputs[gate.input2]
                case Op.OR:
                    output = outputs[gate.input1] | outputs[gate.input2]
                case Op.XOR:
                    output = outputs[gate.input1] ^ outputs[gate.input2]
            outputs[gate.output] = output
    return outputs


def read_num(outputs: dict[str, int], prefix: str) -> int:
    num = ""
    for i in sorted(outputs):
        if i.startswith(prefix):
            num += str(outputs[i])
    return int(num[::-1], 2)


def overwrite_number(bin_value: str, prefix: str, target: dict[str, int]):
    for pos, val in enumerate(bin_value[::-1]):
        key = f"{prefix}{pos:02d}"
        target[key] = int(val)


@dataclass(order=True)
class ExplorationNode:
    cost: int
    swaps: tuple = field(compare=False)


def find_swaps(gates: dict[str, Gate]) -> set[str]:
    wrong_outputs = set()
    for gate in gates.values():
        if gate.output[0] == "z" and gate.op != Op.XOR and gate.output != "z45":
            wrong_outputs.add(gate.output)
        if (
            gate.op == Op.XOR
            and gate.output[0] not in ["x", "y", "z"]
            and gate.input1[0] not in ["x", "y", "z"]
            and gate.input2[0] not in ["x", "y", "z"]
        ):
            wrong_outputs.add(gate.output)
        if gate.op == Op.AND and "x00" not in [gate.input1, gate.input2]:
            for gate2 in gates.values():
                if (
                    gate.output == gate2.input1 or gate.output == gate2.input2
                ) and gate2.op != Op.OR:
                    wrong_outputs.add(gate.output)
        if gate.op == Op.XOR:
            for gate2 in gates.values():
                if (
                    gate.output == gate2.input1 or gate.output == gate2.input2
                ) and gate2.op == Op.OR:
                    wrong_outputs.add(gate.output)
    return wrong_outputs


class Day24(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            inputs, gates = parse_input(file.readlines())
            output = determine_values(inputs, gates)
            print(read_num(output, "z"))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            _, gates = parse_input(file.readlines())
            print(",".join(sorted(find_swaps(gates))))
