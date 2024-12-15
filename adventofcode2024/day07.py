from common import AdventSolution
from tqdm import tqdm


def read_input(lines: list[str]) -> list[list[int]]:
    input: list[list[int]] = []
    for line in lines:
        vals = line.strip().split(" ")
        vals[0] = vals[0][:-1]  # trim trailing colon
        input.append([int(x) for x in vals])
    return input


def find_operators(
    target: int, operands: list[int], allow_concat: bool = False
) -> bool:
    if len(operands) == 1:
        return target == operands[0]
    if allow_concat and find_operators(
        target, [int(str(operands[0]) + str(operands[1]))] + operands[2:], allow_concat
    ):
        return True
    if find_operators(target, [operands[0] + operands[1]] + operands[2:], allow_concat):
        return True
    return find_operators(
        target, [operands[0] * operands[1]] + operands[2:], allow_concat
    )


class Day07(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        with open(input_file, "r") as file:
            params = read_input(file.readlines())
            total = 0
            for target, *operands in params:
                if find_operators(target, operands):
                    total += target
            print(total)

    def part_two(self, input_file: str):
        with open(input_file, "r") as file:
            params = read_input(file.readlines())
            total = 0
            for target, *operands in tqdm(params):
                if find_operators(target, operands, allow_concat=True):
                    total += target
            print(total)
