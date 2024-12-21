from common import AdventSolution


def parse_input(lines: list[str]) -> tuple[set[str], list[str]]:
    towels = set([val.strip() for val in lines[0].strip().split(",")])
    desired_patterns = [line.strip() for line in lines[2:]]

    return towels, desired_patterns


def memoize_make_pattern(target: str, towels: set[str], memory: dict[str, int]) -> int:
    if len(target) == 0:
        return 1

    if target in memory:
        return memory[target]

    num_solutions = 0
    for towel in towels:
        if target.startswith(towel):
            recurse = memoize_make_pattern(target[len(towel) :], towels, memory)
            if recurse > 0:
                num_solutions += recurse

    memory[target] = num_solutions
    return num_solutions


class Day19(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            towels, desired_patterns = parse_input(file.readlines())
            possible_count = 0
            for pattern in desired_patterns:
                if memoize_make_pattern(pattern, towels, {}) > 0:
                    possible_count += 1
            print(possible_count)

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            towels, desired_patterns = parse_input(file.readlines())
            total_solutions = 0
            for pattern in desired_patterns:
                num_solutions = memoize_make_pattern(pattern, towels, {})
                total_solutions += num_solutions
            print(total_solutions)
