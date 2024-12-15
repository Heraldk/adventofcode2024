from dataclasses import dataclass
from itertools import combinations

from common import AdventSolution


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


def parse_input(lines: list[str]) -> tuple[dict[str, list[Coord]], Coord]:
    map: dict[str, list[Coord]] = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char != ".":
                coords = Coord(x, y)
                if char not in map:
                    map[char] = []
                map[char].append(coords)
    return map, Coord(x, y)


def find_antinodes(map: dict[str, list[Coord]], max_dim: Coord) -> int:
    antinode_locs: dict[Coord, bool] = {}

    for antennae, locs in map.items():
        for start, end in combinations(locs, 2):
            delta = Coord(end.x - start.x, end.y - start.y)
            loc1 = Coord(start.x - delta.x, start.y - delta.y)
            loc2 = Coord(end.x + delta.x, end.y + delta.y)
            # print(antennae, loc1, loc2)
            if 0 <= loc1.x <= max_dim.x and 0 <= loc1.y <= max_dim.y:
                antinode_locs[loc1] = True
            if 0 <= loc2.x <= max_dim.x and 0 <= loc2.y <= max_dim.y:
                antinode_locs[loc2] = True

    return len(antinode_locs)


def find_antinodes_part_two(map: dict[str, list[Coord]], max_dim: Coord) -> int:
    antinode_locs: dict[Coord, bool] = {}

    for antennae, locs in map.items():
        for start, end in combinations(locs, 2):
            delta = Coord(end.x - start.x, end.y - start.y)

            loc = start
            while 0 <= loc.x <= max_dim.x and 0 <= loc.y <= max_dim.y:
                antinode_locs[loc] = True
                loc = Coord(loc.x - delta.x, loc.y - delta.y)
            loc = end
            while 0 <= loc.x <= max_dim.x and 0 <= loc.y <= max_dim.y:
                antinode_locs[loc] = True
                loc = Coord(loc.x + delta.x, loc.y + delta.y)

    return len(antinode_locs)


class Day08(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        with open(input_file, "r") as file:
            map, max_dim = parse_input(file.readlines())
            print(find_antinodes(map, max_dim))

    def part_two(self, input_file: str):
        with open(input_file, "r") as file:
            map, max_dim = parse_input(file.readlines())
            print(find_antinodes_part_two(map, max_dim))
