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
    coords = []

    for line in lines:
        vals = line.strip().split(",")
        coords.append(Coord(int(vals[0]), int(vals[1])))

    return coords


def find_path(coords: set[Coord], start: Coord, end: Coord, max_dim: Coord) -> int:
    queue = PriorityQueue()
    queue.put(ExplorationNode(0, start))
    explored: dict[Coord, int] = {start: 0}
    while not queue.empty():
        node = queue.get()
        loc = node.loc
        if loc == end:
            return node.cost

        for direction in DIRECTIONS:
            next_loc = Coord(loc.x + direction.x, loc.y + direction.y)
            if next_loc not in explored and next_loc not in coords:
                if 0 <= next_loc.x <= max_dim.x and 0 <= next_loc.y <= max_dim.y:
                    explored[next_loc] = node.cost + 1
                    queue.put(ExplorationNode(node.cost + 1, next_loc))
    return -1


class Day18(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            coords = read_input(file.readlines())
            max_dims = Coord(6, 6) if kwargs["test_mode"] else Coord(70, 70)
            limit = 12 if kwargs["test_mode"] else 1024
            print(find_path(coords[:limit], Coord(0, 0), max_dims, max_dims))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            coords = read_input(file.readlines())
            max_dims = Coord(6, 6) if kwargs["test_mode"] else Coord(70, 70)
            start, end = (0, len(coords))
            while start + 1 < end:
                mid = ((end - start) // 2) + start
                result = find_path(coords[:mid], Coord(0, 0), max_dims, max_dims)
                if result >= 0:
                    start = mid
                elif result < 0:
                    end = mid
            print(start)
            print(coords[start])
