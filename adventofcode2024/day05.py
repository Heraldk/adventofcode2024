from copy import deepcopy
from dataclasses import dataclass

from common import AdventSolution
from tqdm import tqdm


@dataclass
class Constraint:
    first: int
    second: int


def read_input(lines: list[str]) -> tuple[list[Constraint], list[list[int]]]:
    constraints: list[Constraint] = []
    pages: list[list[int]] = []
    for line in lines:
        if (idx := line.find("|")) >= 0:
            vals = line.strip()
            constraints.append(Constraint(int(vals[:idx]), int(vals[idx + 1 :])))
        elif line.find(",") >= 0:
            pages.append([int(x) for x in line.strip().split(",")])

    return constraints, pages


def _validate_page(
    constraints: list[Constraint], page: list[int]
) -> tuple[bool, Constraint | None]:
    for x, page_num in enumerate(page):
        for page_num2 in page[x + 1 :]:
            for constraint in constraints:
                if page_num == constraint.second and page_num2 == constraint.first:
                    return False, constraint
    return True, None


def validate_page(constraints: list[Constraint], page: list[int]) -> bool:
    val, _ = _validate_page(constraints, page)
    return val


def fix_page(constraints: list[Constraint], page: list[int]) -> list[int]:
    # brute force?
    new_page = deepcopy(page)
    validates, constraint = _validate_page(constraints, new_page)
    while not validates:
        assert constraint is not None
        a, b = new_page.index(constraint.first), new_page.index(constraint.second)
        new_page[a], new_page[b] = new_page[b], new_page[a]
        validates, constraint = _validate_page(constraints, new_page)
    return new_page


class Day05(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        with open(input_file, "r") as file:
            total = 0
            constraints, pages = read_input(file.readlines())
            for page in pages:
                if validate_page(constraints, page):
                    total += page[len(page) // 2]
            print(total)

    def part_two(self, input_file: str):
        with open(input_file, "r") as file:
            total = 0
            constraints, pages = read_input(file.readlines())
            for page in tqdm(pages):
                if not validate_page(constraints, page):
                    new_page = fix_page(constraints, page)
                    total += new_page[len(new_page) // 2]
            print(total)
