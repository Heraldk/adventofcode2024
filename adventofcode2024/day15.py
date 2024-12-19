from dataclasses import dataclass

from common import AdventSolution


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


DIRECTION_MAP = {
    "^": Coord(0, -1),
    "<": Coord(-1, 0),
    ">": Coord(1, 0),
    "v": Coord(0, 1),
}


def parse_input(lines: list[str]) -> tuple[Coord, dict[Coord, str], str]:
    read_map = True
    map = {}
    dirs = ""
    robot_loc = Coord(-1, -1)
    for y, line in enumerate(lines):
        if line.strip() == "":
            read_map = False
            continue
        elif read_map:
            for x, char in enumerate(line.strip()):
                if char == "@":
                    robot_loc = Coord(x, y)
                elif char == "O" or char == "#":
                    map[Coord(x, y)] = char
        else:
            dirs += line.strip()

    return robot_loc, map, dirs


def move_robot(
    robot_loc: Coord, map: dict[Coord, str], directions: str
) -> tuple[Coord, dict[Coord, str]]:
    current_loc = robot_loc
    for dir in directions:
        delta = DIRECTION_MAP[dir]
        next_loc = Coord(current_loc.x + delta.x, current_loc.y + delta.y)
        first_loc = next_loc

        while next_loc in map and map[next_loc] == "O":
            next_loc = Coord(next_loc.x + delta.x, next_loc.y + delta.y)

        if next_loc not in map:
            if first_loc in map:
                map[next_loc] = map[first_loc]
                del map[first_loc]
            current_loc = first_loc
    return current_loc, map


def print_map(robot_loc: Coord, map: dict[Coord, str], boxes: list[Coord] = []) -> None:
    max_y = max([loc.y for loc in map.keys()])
    max_x = max([loc.x for loc in map.keys()])
    inbox = False
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            loc = Coord(x, y)
            if inbox:
                print("]", end="")
                inbox = False
            elif loc == robot_loc:
                print("@", end="")
            elif loc in map:
                print(map[loc], end="")
            elif loc in boxes:
                print("[", end="")
                inbox = True
            else:
                print(".", end="")
        print()


def count_score(map: dict[Coord, str]) -> int:
    score = 0
    for loc, item in map.items():
        if item == "O":
            score += 100 * loc.y + loc.x
    return score


def convert_map_to_part_two(
    robot_loc: Coord, map: dict[Coord, str]
) -> tuple[Coord, list[Coord], dict[Coord, str]]:
    new_map = {}
    boxes = []
    for loc, item in map.items():
        if item == "#":
            new_map[Coord(2 * loc.x, loc.y)] = "#"
            new_map[Coord(2 * loc.x + 1, loc.y)] = "#"
        elif item == "O":
            boxes.append(Coord(2 * loc.x, loc.y))
    return Coord(2 * robot_loc.x, robot_loc.y), boxes, new_map


def move_robot_part_two(
    robot_loc: Coord, map: dict[Coord, str], boxes: list[Coord], directions: str
) -> tuple[Coord, dict[Coord, str], list[Coord]]:
    current_loc = robot_loc
    for dir in directions:
        delta = DIRECTION_MAP[dir]
        next_loc = Coord(current_loc.x + delta.x, current_loc.y + delta.y)

        can_move = True
        push_box_ids = []
        check_box_spaces = [next_loc]
        while len(check_box_spaces) > 0 and can_move:
            check_loc = check_box_spaces.pop()
            if check_loc in map:
                can_move = False
            else:
                if dir in ["^", "v"]:
                    check_loc2 = Coord(check_loc.x - 1, check_loc.y)
                    if check_loc in boxes:
                        box_id = boxes.index(check_loc)
                        if box_id not in push_box_ids:
                            push_box_ids.append(box_id)
                            check_box_spaces.append(
                                Coord(check_loc.x + delta.x, check_loc.y + delta.y)
                            )
                            check_box_spaces.append(
                                Coord(check_loc.x + 1 + delta.x, check_loc.y + delta.y)
                            )

                    elif check_loc2 in boxes:
                        box_id = boxes.index(check_loc2)
                        if box_id not in push_box_ids:
                            push_box_ids.append(box_id)
                            check_box_spaces.append(
                                Coord(check_loc.x + delta.x, check_loc.y + delta.y)
                            )
                            check_box_spaces.append(
                                Coord(check_loc.x + -1 + delta.x, check_loc.y + delta.y)
                            )
                elif dir == "<":
                    place_to_check = Coord(check_loc.x - 1, check_loc.y)
                    if place_to_check in boxes:
                        box_id = boxes.index(place_to_check)
                        if box_id not in push_box_ids:  # it really shouldn't be
                            push_box_ids.append(box_id)
                            check_box_spaces.append(Coord(check_loc.x - 2, check_loc.y))
                elif dir == ">":
                    if check_loc in boxes:
                        box_id = boxes.index(check_loc)
                        if box_id not in push_box_ids:  # it really shouldn't be
                            push_box_ids.append(box_id)
                            check_box_spaces.append(Coord(check_loc.x + 2, check_loc.y))
        if can_move:
            current_loc = next_loc
            for box_id in push_box_ids:
                old_val = boxes[box_id]
                boxes[box_id] = Coord(old_val.x + delta.x, old_val.y + delta.y)

    return current_loc, map, boxes


class Day15(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            robot_loc, map, directions = parse_input(file.readlines())
            robot_loc, map = move_robot(robot_loc, map, directions)
            # print_map(robot_loc, map)
            print(count_score(map))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            robot_loc, map, directions = parse_input(file.readlines())
            robot_loc, boxes, map = convert_map_to_part_two(robot_loc, map)
            robot_loc, map, boxes = move_robot_part_two(
                robot_loc, map, boxes, directions
            )
            score = 0
            for box in boxes:
                score += 100 * box.y + box.x
            print(score)
