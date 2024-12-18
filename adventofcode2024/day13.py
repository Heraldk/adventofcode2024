import re
from dataclasses import dataclass

from common import AdventSolution


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


@dataclass
class MachineConfig:
    a_button: Coord
    b_button: Coord
    prize_loc: Coord


def read_input(lines: list[str], offset: int = 0) -> list[MachineConfig]:
    # remove all empty lines
    machines: list[MachineConfig] = []
    index = 0
    while index < len(lines):
        a_button = re.match(r"Button A: X\+(\d+), Y\+(\d+)", lines[index])
        b_button = re.match(r"Button B: X\+(\d+), Y\+(\d+)", lines[index + 1])
        prize_loc = re.match(r"Prize: X=(\d+), Y=(\d+)", lines[index + 2])

        m = MachineConfig(
            Coord(int(a_button.group(1)), int(a_button.group(2))),
            Coord(int(b_button.group(1)), int(b_button.group(2))),
            Coord(int(prize_loc.group(1)) + offset, int(prize_loc.group(2)) + offset),
        )
        machines.append(m)
        index += 4
    return machines


def solve_equation(machine: MachineConfig) -> tuple[int, int] | None:
    # solved on paper general system of linear equations, nets me:
    # a_x * prize_y - a_x * b_y * B + a_y * b_x * B = a_y * prize_x
    #     1               2               3               4

    # 1
    term_1 = machine.a_button.x * machine.prize_loc.y
    term_2 = -machine.a_button.x * machine.b_button.y
    term_3 = machine.a_button.y * machine.b_button.x
    term_4 = machine.a_button.y * machine.prize_loc.x

    # move term 1 to right side and combine with term 4
    rhs = term_4 - term_1
    # combine lhs
    lhs = term_2 + term_3
    # solve for B
    if (rhs % lhs) != 0:
        return None
    B_press = int(rhs / lhs)

    # A equation then is
    # a_x * A  = prize_x - b_x * B
    #   5                6
    term_6 = machine.prize_loc.x - (machine.b_button.x * B_press)

    if (term_6 % machine.a_button.x) != 0:
        return None
    A_press = int(term_6 / machine.a_button.x)

    return A_press, B_press


class Day13(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            input = read_input(file.readlines())
            tokens = 0
            for m in input:
                solve = solve_equation(m)
                if solve:
                    tokens += solve[0] * 3 + solve[1]
            print(tokens)

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            input = read_input(file.readlines(), offset=10000000000000)
            tokens = 0
            for m in input:
                solve = solve_equation(m)
                if solve:
                    tokens += solve[0] * 3 + solve[1]
            print(tokens)
