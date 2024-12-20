from dataclasses import dataclass, field
from queue import PriorityQueue

from common import AdventSolution


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


@dataclass(frozen=True)
class Position:
    location: Coord
    facing: int


@dataclass(order=True)
class ExplorationNode:
    cost: int
    pos: Position = field(compare=False)
    history: set[Coord] = field(compare=False)


DIRECTIONS = [Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1)]


def read_map(lines: list[str]) -> tuple[dict[Coord, str], Coord, Coord]:
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


def find_shortest_path(
    map: dict[Coord, str], start: Coord, end: Coord, find_all_paths: bool = False
) -> int:
    queue = PriorityQueue()
    pos = Position(start, 0)
    queue.put(ExplorationNode(0, pos, set()))
    explored: dict[Position, int] = {pos: 0}

    solution_visited: set[Coord] = set()
    best_path = 0

    while not queue.empty():
        node = queue.get()
        loc = node.pos.location
        facing = node.pos.facing
        if best_path > 0 and node.cost > best_path:
            # we're done!
            return len(solution_visited) + 1  # +1 for the end position!

        if loc == end:
            if not find_all_paths:
                return node.cost

            if best_path == 0:
                best_path = node.cost
            assert node.cost == best_path
            solution_visited |= node.history

        move_loc = Coord(loc.x + DIRECTIONS[facing].x, loc.y + DIRECTIONS[facing].y)
        move_pos = Position(move_loc, facing)
        turn_left = Position(loc, (facing + 4 - 1) % 4)
        turn_right = Position(loc, (facing + 1) % 4)
        moves = [move_pos, turn_left, turn_right]
        cost = [1, 1000, 1000]
        history = set(node.history)
        history.add(loc)
        for m, c in zip(moves, cost):
            if m.location not in map:
                if (
                    m not in explored
                    or explored[m] > node.cost + c
                    or (find_all_paths and explored[m] >= node.cost + c)
                ):
                    explored[m] = node.cost + c
                    queue.put(ExplorationNode(node.cost + c, m, set(history)))

    return -1


class Day16(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            map, start, end = read_map(file.readlines())
            print(find_shortest_path(map, start, end))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            map, start, end = read_map(file.readlines())
            print(find_shortest_path(map, start, end, find_all_paths=True))
