from itertools import product

from common import AdventSolution


def parse_input(lines: list[str]) -> tuple[list[list[int]], list[list[int]]]:
    keys = []
    locks = []
    x = 0
    while x < len(lines):
        current = [-1 for _ in range(5)]
        is_lock = True if lines[x].strip() == "#" * 5 else False
        assert (
            lines[x + 6].strip() == "#" * 5
            if not is_lock
            else lines[x + 6].strip() == "." * 5
        )
        assert lines[x].strip() == "#" * 5 if is_lock else lines[x].strip() == "." * 5

        for col in range(5):
            for row in range(7):
                if lines[x + row][col] == "#":
                    current[col] += 1
        x += 8

        if is_lock:
            locks.append(current)
        else:
            keys.append(current)

    return keys, locks


def is_overlap(key: list[int], lock: list[int]) -> bool:
    for a, b in zip(key, lock):
        if a + b > 5:
            return True
    return False


class Day25(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            keys, locks = parse_input(file.readlines())
            total = 0
            for key, lock in product(keys, locks):
                if not is_overlap(key, lock):
                    total += 1
            print(total)

    @classmethod
    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            pass
