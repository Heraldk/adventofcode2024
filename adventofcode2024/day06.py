from copy import deepcopy
from dataclasses import dataclass

from common import AdventSolution
from tqdm import tqdm


@dataclass(frozen=True)
class Coord:
    x: int
    y: int
    heading: int = -1


def read_map(input: list[str]) -> tuple[dict[Coord, str], Coord, int, int]:
    map = {}
    for y, row in enumerate(input):
        for x, col in enumerate(row.strip()):
            if col == "#":
                map[Coord(x, y)] = col
            elif col == "^":
                starting_loc = Coord(x, y)
    return map, starting_loc, x, y


HEADINGS = [Coord(0, -1), Coord(1, 0), Coord(0, 1), Coord(-1, 0)]


def walk_the_map(map: list[str], starting_loc: Coord, max_x: int, max_y: int) -> int:
    visited: dict[Coord, bool] = {}

    heading = 0
    location = starting_loc

    while (
        location.x >= 0
        and location.x <= max_x
        and location.y >= 0
        and location.y <= max_y
    ):
        next_loc = Coord(
            location.x + HEADINGS[heading].x, location.y + HEADINGS[heading].y
        )
        while next_loc in map:
            heading = (heading + 1) % 4
            next_loc = Coord(
                location.x + HEADINGS[heading].x, location.y + HEADINGS[heading].y
            )
        visited[location] = True
        location = next_loc

    return len(visited)


def walk_the_map_detect_loops(
    map: list[str], starting_loc: Coord, max_x: int, max_y: int
) -> int:
    visited: dict[Coord, bool] = {}

    heading = 0
    location = Coord(starting_loc.x, starting_loc.y, heading)

    while (
        location.x >= 0
        and location.x <= max_x
        and location.y >= 0
        and location.y <= max_y
    ):
        next_loc = Coord(
            location.x + HEADINGS[heading].x, location.y + HEADINGS[heading].y, -1
        )
        next_heading = heading
        while next_loc in map:
            next_heading = (next_heading + 1) % 4
            next_loc = Coord(
                location.x + HEADINGS[next_heading].x,
                location.y + HEADINGS[next_heading].y,
                -1,
            )
        visited[Coord(location.x, location.y, heading)] = True
        if Coord(next_loc.x, next_loc.y, next_heading) in visited:
            return -1
        location = next_loc
        heading = next_heading

    return len(visited)


class Day06(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            map, starting_loc, max_x, max_y = read_map(file.readlines())
            print(walk_the_map(map, starting_loc, max_x, max_y))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            map, starting_loc, max_x, max_y = read_map(file.readlines())
            results = []
            for y in tqdm(range(max_y + 1)):
                for x in range(max_x + 1):
                    coord = Coord(x, y)
                    if coord not in map:
                        mod_map = deepcopy(map)
                        mod_map[coord] = "O"
                        if (
                            walk_the_map_detect_loops(
                                mod_map, starting_loc, max_x, max_y
                            )
                        ) < 0:
                            results.append(coord)
            print(len(results))


# Day06().part_two("test_input_files/day06.txt")
