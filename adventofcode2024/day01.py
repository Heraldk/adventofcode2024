from collections import Counter

from common import AdventSolution


def read_lists(lines: list[str]) -> tuple[list[int], list[int]]:
    list1: list[int] = []
    list2: list[int] = []
    for line in lines:
        vals = line.strip().split()
        list1.append(int(vals[0]))
        list2.append(int(vals[1]))
    return list1, list2


def calculate_distance(list1: list[int], list2: list[int]) -> int:
    distance = 0
    for x, y in zip(list1, list2):
        distance += abs(x - y)
    return distance


def calculate_similarity(list1: list[int], list2: list[int]) -> int:
    counter = Counter(list2)
    similarity = 0
    for x in list1:
        similarity += x * counter.get(x, 0)
    return similarity


class Day01(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            list1, list2 = read_lists(file.readlines())
            list1.sort()
            list2.sort()
            print(calculate_distance(list1, list2))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            list1, list2 = read_lists(file.readlines())
            print(calculate_similarity(list1, list2))
