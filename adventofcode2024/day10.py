from dataclasses import dataclass

from common import AdventSolution


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


DIRECTIONS = [Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1)]
DIRECTION_LABELS = ["E", "S", "W", "N"]


def parse_map(lines: list[str]) -> dict[Coord, int]:
    map: dict[Coord, str] = {}
    for y, row in enumerate(lines):
        for x, col in enumerate(row.strip()):
            map[Coord(x, y)] = int(col)
    return map


def count_trail_score(
    map: dict[Coord, int], height: int, loc: Coord, path: str
) -> tuple[set[Coord], set[str]]:
    if height == 9:
        assert map[loc] == 9
        return {loc}, {path}

    locs: set[Coord] = set()
    paths: set[str] = set()
    for dir, label in zip(DIRECTIONS, DIRECTION_LABELS):
        coord_next = Coord(loc.x + dir.x, loc.y + dir.y)
        if coord_next in map and map[coord_next] == height + 1:
            new_locs, new_paths = count_trail_score(
                map, height + 1, coord_next, path + label
            )
            locs |= new_locs
            paths |= new_paths
    return locs, paths


def count_trail_scores(map: dict[Coord, int]) -> tuple[int, int]:
    total_scores, total_rating = 0, 0
    for loc, height in map.items():
        if height == 0:
            score, rating = count_trail_score(map, height, loc, "")
            total_scores += len(score)
            total_rating += len(rating)
    return total_scores, total_rating


class Day10(AdventSolution):
    @classmethod
    def part_one(self, input_file: str):
        with open(input_file, "r") as file:
            map = parse_map(file.readlines())
            print(count_trail_scores(map)[0])

    def part_two(self, input_file: str):
        with open(input_file, "r") as file:
            map = parse_map(file.readlines())
            print(count_trail_scores(map)[1])


# Day10().part_one("test_input_files/day10.txt")
