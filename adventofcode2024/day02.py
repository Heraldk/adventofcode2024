from itertools import pairwise

from common import AdventSolution


def parse_level(line: str) -> list[int]:
    return [int(x) for x in line.strip().split()]


def is_safe(level: list[int]) -> bool:
    vals: list[int] = []
    for a, b in pairwise(level):
        vals.append(a - b)
    return all(x > 0 and x < 4 for x in vals) or all(x > -4 and x < 0 for x in vals)


def is_safe_with_dampener(level: list[int]) -> bool:
    for x in range(len(level)):
        if is_safe(level[0:x] + level[x + 1 :]):
            return True
    return False


class Day02(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            safe_count = 0
            for line in file.readlines():
                level = parse_level(line)
                safe_count += 1 if is_safe(level) else 0
            print(safe_count)

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            safe_count = 0
            for line in file.readlines():
                level = parse_level(line)
                safe_count += 1 if is_safe_with_dampener(level) else 0
            print(safe_count)
