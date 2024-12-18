from dataclasses import dataclass
from typing import Any

from common import AdventSolution


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


DIRECTIONS = [Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1)]
DIRECTION_LABELS = ["E", "S", "W", "N"]
DIRECTION_LABEL_TO_DIRECTIONS = {
    "E": DIRECTIONS[0],
    "S": DIRECTIONS[1],
    "W": DIRECTIONS[2],
    "N": DIRECTIONS[3],
}


def parse_map(lines: list[str]) -> dict[Coord, str]:
    map: dict[Coord, str] = {}
    for y, row in enumerate(lines):
        for x, col in enumerate(row.strip()):
            map[Coord(x, y)] = col
    return map


def find_areas_and_perims(
    map: dict[Coord, str]
) -> tuple[list[list[Coord]], list[list[tuple[Coord, Coord, Coord]]]]:
    explored: dict[Coord, int] = {}
    areas: list[list[Coord]] = []
    fences: list[list[tuple[Coord, Coord, Coord]]] = []

    area_id = 0
    for loc, label in map.items():
        if loc in explored:
            continue
        queue: list[Coord] = [loc]
        areas.append([])
        fences.append([])
        while len(queue) > 0:
            curr_loc = queue.pop()
            explored[curr_loc] = area_id
            areas[area_id].append(curr_loc)
            for dir in DIRECTIONS:
                next_coord = Coord(curr_loc.x + dir.x, curr_loc.y + dir.y)
                if next_coord not in map:
                    fences[area_id].append((curr_loc, next_coord, dir))
                elif map[next_coord] != label:
                    fences[area_id].append((curr_loc, next_coord, dir))
                elif next_coord not in explored and next_coord not in queue:
                    queue.append(next_coord)
        area_id += 1

    return areas, fences


def calc_price(areas: list[list[Any]], fences: list[list[Any]]) -> int:
    total = 0
    for area, fences in zip(areas, fences):
        total += len(area) * len(fences)
    return total


@dataclass
class Segment:
    start: Coord
    end: Coord
    fence_direction: Coord


DIRECTION_TO_START_MAPPING = {
    DIRECTION_LABEL_TO_DIRECTIONS["N"]: [
        DIRECTION_LABEL_TO_DIRECTIONS["W"],
        DIRECTION_LABEL_TO_DIRECTIONS["E"],
    ],
    DIRECTION_LABEL_TO_DIRECTIONS["E"]: [
        DIRECTION_LABEL_TO_DIRECTIONS["N"],
        DIRECTION_LABEL_TO_DIRECTIONS["S"],
    ],
    DIRECTION_LABEL_TO_DIRECTIONS["W"]: [
        DIRECTION_LABEL_TO_DIRECTIONS["N"],
        DIRECTION_LABEL_TO_DIRECTIONS["S"],
    ],
    DIRECTION_LABEL_TO_DIRECTIONS["S"]: [
        DIRECTION_LABEL_TO_DIRECTIONS["W"],
        DIRECTION_LABEL_TO_DIRECTIONS["E"],
    ],
}


def merge_fences(fences: list[list[tuple[Coord, Coord, Coord]]]) -> list[list[Segment]]:
    fence_segments = []
    for fence_list in fences:
        current_segments: list[Segment] = [
            Segment(inside, inside, direction) for inside, _, direction in fence_list
        ]
        next_segments: list[Segment] = []
        while True:
            next_segments = []
            for segment1 in current_segments:
                found = False
                for segment2 in next_segments:
                    if segment1.fence_direction == segment2.fence_direction:
                        start_dir, end_dir = DIRECTION_TO_START_MAPPING[
                            segment1.fence_direction
                        ]

                        if (
                            Coord(
                                segment1.start.x + start_dir.x,
                                segment1.start.y + start_dir.y,
                            )
                            == segment2.end
                        ):
                            found = True
                            segment2.end = segment1.end
                            break
                        elif (
                            Coord(
                                segment1.end.x + end_dir.x, segment1.end.y + end_dir.y
                            )
                            == segment2.start
                        ):
                            found = True
                            segment2.start = segment1.start
                            break
                if not found:
                    next_segments.append(segment1)
            if len(current_segments) == len(next_segments):
                break
            current_segments = next_segments
        fence_segments.append(current_segments)
    return fence_segments


class Day12(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            map = parse_map(file.readlines())
            areas, fences = find_areas_and_perims(map)
            print(calc_price(areas, fences))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            map = parse_map(file.readlines())
            areas, fences = find_areas_and_perims(map)
            new_fences = merge_fences(fences)
            print(calc_price(areas, new_fences))
