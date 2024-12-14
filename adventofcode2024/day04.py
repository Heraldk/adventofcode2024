from dataclasses import dataclass

from common import AdventSolution


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


def _ensure_init(d: dict[Coords, list[Coords]], coords: Coords):
    if coords not in d:
        d[coords] = []


# efficient in that this does the calculation in one interation of the input data O(n)
# inefficient in that the code is a bit complex :P
def find_xmases(input: list[str]) -> int:
    forward: dict[str, dict[Coords, list[Coords]]] = {
        "M": {},
        "A": {},
        "S": {},
        "#": {},
    }
    forward_progression = {"M": "A", "A": "S", "S": "#"}
    backward_progression = {"A": "M", "M": "X", "X": "#"}
    backward: dict[str, dict[Coords, list[Coords]]] = {
        "A": {},
        "M": {},
        "X": {},
        "#": {},
    }
    directions = [Coords(1, 0), Coords(1, 1), Coords(0, 1), Coords(-1, 1)]

    for y, row in enumerate(input):
        for x, char in enumerate(row):
            coords = Coords(x, y)
            if char == "X":
                for dir in directions:
                    next_coords = Coords(coords.x + dir.x, coords.y + dir.y)
                    _ensure_init(forward["M"], next_coords)
                    forward["M"][next_coords].append(dir)
            if char == "S":
                for dir in directions:
                    next_coords = Coords(coords.x + dir.x, coords.y + dir.y)
                    _ensure_init(backward["A"], next_coords)
                    backward["A"][next_coords].append(dir)

            if char in forward and coords in forward[char]:
                for direction in forward[char][coords]:
                    next_char = forward_progression[char]
                    next_coords = Coords(coords.x + direction.x, coords.y + direction.y)
                    _ensure_init(forward[next_char], next_coords)
                    forward[next_char][next_coords].append(direction)
            if char in backward and coords in backward[char]:
                for direction in backward[char][coords]:
                    next_char = backward_progression[char]
                    next_coords = Coords(coords.x + direction.x, coords.y + direction.y)
                    _ensure_init(backward[next_char], next_coords)
                    backward[next_char][next_coords].append(direction)

    total = 0
    for finished in forward["#"].values():
        total += len(finished)
    for finished in backward["#"].values():
        total += len(finished)
    return total


def _lookup(input: list[str], coords: Coords, direction: Coords) -> str | None:
    if coords.y + direction.y < 0 or coords.y + direction.y >= len(input):
        return None
    if coords.x + direction.x < 0 or coords.x + direction.x >= len(input[0]):
        return None
    return input[coords.y + direction.y][coords.x + direction.x]


def find_cross_mases(input: list[str]) -> int:

    total = 0
    for y, row in enumerate(input):
        for x, char in enumerate(row):
            if char == "A":
                coords = Coords(x, y)
                upper_left = _lookup(input, coords, Coords(-1, -1))
                lower_right = _lookup(input, coords, Coords(1, 1))
                upper_right = _lookup(input, coords, Coords(1, -1))
                lower_left = _lookup(input, coords, Coords(-1, 1))

                if (upper_left, lower_right) in [("M", "S"), ("S", "M")] and (
                    upper_right,
                    lower_left,
                ) in [("M", "S"), ("S", "M")]:
                    total += 1

    return total


class Day04(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        with open(input_file, "r") as file:
            print(find_xmases(file.readlines()))

    def part_two(self, input_file: str):
        with open(input_file, "r") as file:
            print(find_cross_mases(file.readlines()))


with open("test_input_files/day04.txt") as file:
    find_cross_mases(file.readlines())
