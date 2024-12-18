import re

from common import AdventSolution


def find_muls(input: str) -> list[str]:
    matches = re.findall(r"mul\(\d+,\d+\)", input)
    return matches


def find_muls_with_dos_donts(input: str) -> list[str]:
    matches = re.findall(r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))", input)
    return [x[0] if x[0] else x[1] if x[1] else x[2] for x in matches]


def eval_mul(input: str) -> int:
    m = re.match(r"mul\((\d+),(\d+)\)", input)
    return int(m.group(1)) * int(m.group(2))


class Day03(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            vals = [eval_mul(x) for x in find_muls("".join(file.readlines()))]
            print(sum(vals))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            do_on = True
            total = 0
            for x in find_muls_with_dos_donts("".join(file.readlines())):
                if x == "do()":
                    do_on = True
                elif x == "don't()":
                    do_on = False
                elif do_on:
                    total += eval_mul(x)
            print(total)
