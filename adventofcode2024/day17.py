import re
from dataclasses import dataclass
from enum import IntEnum

from common import AdventSolution


class Instructions(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


@dataclass
class ProgState:
    reg_A: int
    reg_B: int
    reg_C: int
    in_p: int  # instruction pointer


def read_input(lines: list[str]) -> tuple[ProgState, list[int]]:
    m1 = re.match(r"Register A: (\d+)", lines[0])
    m2 = re.match(r"Register B: (\d+)", lines[1])
    m3 = re.match(r"Register C: (\d+)", lines[2])
    prog = lines[4].strip()[9:]
    return ProgState(int(m1.group(1)), int(m2.group(1)), int(m3.group(1)), 0), [
        int(x) for x in prog.split(",")
    ]


def get_compound_operand_value(state: ProgState, operand: int) -> int:
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return state.reg_A
    elif operand == 5:
        return state.reg_B
    elif operand == 6:
        return state.reg_C
    assert False


def run_program(state: ProgState, program: list[int]) -> list[int]:
    output = []
    while state.in_p >= 0 and state.in_p < len(program):
        instruction = program[state.in_p]
        operand = program[state.in_p + 1]
        jump = False
        match (instruction):
            case Instructions.ADV:
                compound_value = get_compound_operand_value(state, operand)
                state.reg_A = state.reg_A // pow(2, compound_value)
            case Instructions.BXL:
                state.reg_B = state.reg_B ^ operand
            case Instructions.BST:
                compound_value = get_compound_operand_value(state, operand)
                state.reg_B = compound_value % 8
            case Instructions.JNZ:
                if state.reg_A != 0 and state.in_p != operand:
                    jump = True
                    state.in_p = operand  # -2 since we'll re-add the two afterwards
            case Instructions.BXC:
                state.reg_B = state.reg_B ^ state.reg_C
            case Instructions.OUT:
                compound_value = get_compound_operand_value(state, operand)
                output_val = compound_value % 8
                output.append(output_val)
            case Instructions.BDV:
                compound_value = get_compound_operand_value(state, operand)
                state.reg_B = state.reg_A // pow(2, compound_value)
            case Instructions.CDV:
                compound_value = get_compound_operand_value(state, operand)
                state.reg_C = state.reg_A // pow(2, compound_value)
        if not jump:
            state.in_p += 2
    return output


def recursive_solve(
    program: list[int], start_a: int, index: int, possible_match: set[int] = set()
):
    for n in range(8):
        next_a = (start_a << 3) | n
        output = run_program(ProgState(next_a, 0, 0, 0), program)
        if output == program[-index:]:
            if output == program:
                possible_match.add(next_a)
            else:
                recursive_solve(program, next_a, index + 1, possible_match)
    if len(possible_match) > 0:
        return min(possible_match)
    else:
        return 0


class Day17(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            state, program = read_input(file.readlines())
            output = run_program(state, program)
            print(",".join([str(x) for x in output]))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            _, program = read_input(file.readlines())
            result = recursive_solve(program, 0, 1)
            print(result)
