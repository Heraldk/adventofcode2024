from dataclasses import dataclass, field
from queue import PriorityQueue

from common import AdventSolution
from tqdm import tqdm


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


@dataclass(order=True)
class ExplorationNode:
    cost: int
    loc: Coord = field(compare=False)


DIRECTIONS = [Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1)]


def read_input(lines: list[str]) -> list[Coord]:
    map = {}
    start = Coord(0, 0)
    end = Coord(0, 0)
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            loc = Coord(x, y)
            if char == "S":
                start = loc
            elif char == "E":
                end = loc
            elif char == "#":
                map[loc] = "#"

    return map, start, end


def find_path(map: dict[Coord, str], start: Coord, end: Coord) -> dict[Coord, int]:
    queue = PriorityQueue()
    queue.put(ExplorationNode(0, start))
    explored: dict[Coord, int] = {start: 0}
    while not queue.empty():
        node = queue.get()
        loc = node.loc
        if loc == end:
            return explored

        for direction in DIRECTIONS:
            next_loc = Coord(loc.x + direction.x, loc.y + direction.y)
            if next_loc not in explored and next_loc not in map:
                explored[next_loc] = node.cost + 1
                queue.put(ExplorationNode(node.cost + 1, next_loc))
    return explored


POSSIBLE_CHEATS = {
    Coord(1, 0): [Coord(2, 0), Coord(1, 1), Coord(1, -1)],
    Coord(0, 1): [Coord(0, 2), Coord(-1, 1), Coord(1, -1)],
    Coord(-1, 0): [Coord(-2, 0), Coord(-1, 1), Coord(-1, -1)],
    Coord(0, -1): [Coord(0, -2), Coord(1, -1), Coord(-1, -1)],
}


def print_map(map: dict[Coord, str], highlight: Coord | None = None) -> None:
    max_y = max([loc.y for loc in map.keys()])
    max_x = max([loc.x for loc in map.keys()])
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            loc = Coord(x, y)
            if loc == highlight:
                print("1", end="")
            elif loc in map:
                print(map[loc], end="")
            else:
                print(".", end="")
        print()


def find_cheats_part_one(
    map: dict[Coord, str], path: dict[Coord, int]
) -> dict[int, list[Coord]]:
    cheats_by_distance: dict[int, list[Coord]] = {}
    for loc, distance_to_goal in path.items():
        for dir in DIRECTIONS:
            next_loc = Coord(loc.x + dir.x, loc.y + dir.y)
            if map.get(next_loc, "") == "#":
                for cheat_attempt in POSSIBLE_CHEATS[dir]:
                    jump_loc = Coord(loc.x + cheat_attempt.x, loc.y + cheat_attempt.y)
                    jump_distance_to_goal = path.get(jump_loc, distance_to_goal)
                    savings = distance_to_goal - (jump_distance_to_goal + 2)
                    if savings > 0:
                        if savings not in cheats_by_distance:
                            cheats_by_distance[savings] = []
                        cheats_by_distance[savings].append(next_loc)
    return cheats_by_distance


def find_cheats_part_two(
    map: dict[Coord, str], path: dict[Coord, int], max_cheat_distance: int
) -> dict[int, set[tuple[Coord, Coord]]]:
    cheats_by_distance: dict[int, list[Coord]] = {}
    for loc, distance_to_goal in tqdm(path.items()):
        for loc2, jump_distance_to_goal in path.items():
            distance_to_cheat = abs(loc2.y - loc.y) + abs(loc2.x - loc.x)
            savings = distance_to_goal - (jump_distance_to_goal + distance_to_cheat)
            if distance_to_cheat <= max_cheat_distance and savings > 0:
                if savings not in cheats_by_distance:
                    cheats_by_distance[savings] = set()
                cheats_by_distance[savings].add((loc, loc2))
    return cheats_by_distance


class Day20(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            map, start, end = read_input(file.readlines())
            route = find_path(
                map, end, start
            )  # reverse as we want distance to the end from each position
            cheats_by_distance = find_cheats_part_one(map, route)
            total_meet_threshold = 0
            for cheat_savings, cheats in cheats_by_distance.items():
                if kwargs["test_mode"]:
                    print(cheat_savings, len(cheats))
                elif cheat_savings >= 100:
                    total_meet_threshold += len(cheats)
            if not kwargs["test_mode"]:
                print(total_meet_threshold)

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            map, start, end = read_input(file.readlines())
            route = find_path(
                map, end, start
            )  # reverse as we want distance to the end from each position
            cheats_by_distance = find_cheats_part_two(map, route, 20)
            total_meet_threshold = 0
            threshold = 50 if kwargs["test_mode"] else 100
            for cheat_savings, cheats in sorted(cheats_by_distance.items()):
                if cheat_savings >= threshold:
                    total_meet_threshold += len(cheats)
            print(total_meet_threshold)
