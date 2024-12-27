from dataclasses import dataclass, field
from queue import PriorityQueue

from common import AdventSolution


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


KEYPAD_MAP = {
    Coord(0, 0): "7",
    Coord(1, 0): "8",
    Coord(2, 0): "9",
    Coord(0, 1): "4",
    Coord(1, 1): "5",
    Coord(2, 1): "6",
    Coord(0, 2): "1",
    Coord(1, 2): "2",
    Coord(2, 2): "3",
    Coord(1, 3): "0",
    Coord(2, 3): "A",
}

REV_KEYPAD_MAP = {
    "7": Coord(0, 0),
    "8": Coord(1, 0),
    "9": Coord(2, 0),
    "4": Coord(0, 1),
    "5": Coord(1, 1),
    "6": Coord(2, 1),
    "1": Coord(0, 2),
    "2": Coord(1, 2),
    "3": Coord(2, 2),
    "0": Coord(1, 3),
    "A": Coord(2, 3),
}

DIRECTION_MAP = {
    Coord(1, 0): "^",
    Coord(2, 0): "A",
    Coord(0, 1): "<",
    Coord(1, 1): "v",
    Coord(2, 1): ">",
}

REV_DIRECTION_MAP = {
    "^": Coord(1, 0),
    "A": Coord(2, 0),
    "<": Coord(0, 1),
    "v": Coord(1, 1),
    ">": Coord(2, 1),
}

NUMERIC_KEYPAD_START = Coord(2, 3)
DIRECTION_KEYPAD_START = Coord(2, 0)

ACTION_TO_DIRECTION = {
    "^": Coord(0, -1),
    ">": Coord(1, 0),
    "v": Coord(0, 1),
    "<": Coord(-1, 0),
    "A": Coord(0, 0),
}


def parse_input(lines: list[str]) -> list[str]:
    return [x.strip() for x in lines]


@dataclass(order=True)
class ExplorationNode:
    cost: int
    pos: tuple = field(compare=False)


def make_move(pos: tuple, maps: list[dict[Coord, str]], move: str) -> tuple | None:
    goal = pos[-1]
    locs = pos[:-1]
    next_pos = []
    done = False
    depth = 0
    while not done:
        done = True
        if move == "A":
            move = maps[depth][pos[depth]]
            next_loc = locs[depth]
            depth += 1
            done = False
            if depth >= len(locs):
                if move != goal[0]:
                    return None
                else:
                    goal = goal[1:]
                    done = True
        else:
            dir = ACTION_TO_DIRECTION[move]
            loc = locs[depth]
            next_loc = Coord(loc.x + dir.x, loc.y + dir.y)
            if next_loc not in maps[depth]:
                return None
        next_pos.append(next_loc)

    next_pos.extend(locs[depth + 1 :])
    next_pos.append(goal)
    return tuple(next_pos)


# pos is a tuple of the coordinates of each robot arm's position on each keypad plus
# the last item is the goal state: which next button press is the correct goal state
# cache is a fast lookup of any previously seen pos tuples to how far away the solution
# is
def find_shortest_path(pos: tuple, maps: list[dict[Coord, str]]) -> int:
    queue = PriorityQueue()
    queue.put(ExplorationNode(0, pos))
    explored: dict[tuple, int] = {pos: 0}
    while not queue.empty():
        node = queue.get()
        curr_pos = node.pos
        if curr_pos[-1] == "":
            return node.cost

        for move in ACTION_TO_DIRECTION.keys():
            next_loc = make_move(curr_pos, maps, move)
            if next_loc and next_loc not in explored:
                explored[next_loc] = node.cost + 1
                queue.put(ExplorationNode(node.cost + 1, next_loc))
    return -1


def calc_score(length: int, target: str):
    return length * int(target[:-1])


def find_paths_from_key_to_key(
    map: dict[str, Coord], pos: Coord, target: str
) -> list[str]:
    paths = []
    queue = [(pos, "")]
    end_pos = map[target]
    while queue:
        cur_pos, path = queue.pop()
        if cur_pos == end_pos:
            paths.append(path)
            continue

        if cur_pos.x != end_pos.x:
            if cur_pos.x > end_pos.x:
                next_pos = Coord(cur_pos.x - 1, cur_pos.y)
                dir = "<"
            else:
                next_pos = Coord(cur_pos.x + 1, cur_pos.y)
                dir = ">"
            if next_pos in map.values():
                queue.append((next_pos, path + dir))

        if cur_pos.y != end_pos.y:
            if cur_pos.y > end_pos.y:
                next_pos = Coord(cur_pos.x, cur_pos.y - 1)
                dir = "^"
            else:
                next_pos = Coord(cur_pos.x, cur_pos.y + 1)
                dir = "v"
            if next_pos in map.values():
                queue.append((next_pos, path + dir))

    return paths


def find_keypad_path_with_cache(
    cache: dict[tuple, int], map: dict[str, Coord], code: str, num_robots: int
) -> int:
    cache_key = (len(map), code, num_robots)
    if cache_key in cache:
        return cache[cache_key]

    if num_robots == 0:
        cache[cache_key] = len(code)
        return len(code)

    current_pos = map["A"]
    min_path = 0
    for letter in code:
        min_next_segment = -1
        possible_solutions = find_paths_from_key_to_key(map, current_pos, letter)
        for seq in possible_solutions:
            length = find_keypad_path_with_cache(
                cache, REV_DIRECTION_MAP, seq + "A", num_robots - 1
            )
            if min_next_segment < 0 or length < min_next_segment:
                min_next_segment = length
        min_path += min_next_segment
        current_pos = map[letter]

    cache[cache_key] = min_path
    return min_path


class Day21(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            score = 0
            for line in file.readlines():
                length = find_shortest_path(
                    (
                        DIRECTION_KEYPAD_START,
                        DIRECTION_KEYPAD_START,
                        NUMERIC_KEYPAD_START,
                        line.strip(),
                    ),
                    [DIRECTION_MAP, DIRECTION_MAP, KEYPAD_MAP],
                )
                # print(length)
                score += calc_score(length, line.strip())
            print(score)

    def part_two(self, input_file: str, **kwargs):
        score = 0
        with open(input_file, "r") as file:
            NUM_ROBOTS = 26
            for line in file.readlines():
                length = find_keypad_path_with_cache(
                    {}, REV_KEYPAD_MAP, line.strip(), NUM_ROBOTS
                )
                # print(length)
                score += calc_score(length, line.strip())
            print(score)
