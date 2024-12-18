import math
import re
from dataclasses import dataclass

from common import AdventSolution


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


@dataclass
class Robot:
    loc: Coord
    vel: Coord


DIRECTIONS = [Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1)]


def parse_input(lines: list[str]) -> list[Robot]:
    robots = []
    for line in lines:
        vals = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line.strip())
        robots.append(
            Robot(
                Coord(int(vals.group(1)), int(vals.group(2))),
                Coord(int(vals.group(3)), int(vals.group(4))),
            )
        )
    return robots


def calc_robot_positions(
    robots: list[Robot], seconds: int, max_dim: Coord
) -> tuple[list[Robot], dict[Coord, bool]]:
    moved_robots = []
    robot_lookup = {}
    for robot in robots:
        loc = Coord(
            (robot.loc.x + robot.vel.x * seconds) % max_dim.x,
            (robot.loc.y + robot.vel.y * seconds) % max_dim.y,
        )
        moved_robots.append(
            Robot(
                loc,
                robot.vel,
            )
        )
        robot_lookup[loc] = True

    return moved_robots, robot_lookup


def count_robots_in_quadrants(robots: list[Robot], max_dim: Coord):
    by_quadrant_count = [0 for _ in range(4)]
    x_split = max_dim.x // 2
    y_split = max_dim.y // 2
    for robot in robots:
        index = -1
        if robot.loc.y < y_split:
            index = 0 if robot.loc.x < x_split else 1 if robot.loc.x > x_split else -1
        elif robot.loc.y > y_split:
            index = 2 if robot.loc.x < x_split else 3 if robot.loc.x > x_split else -1
        if index >= 0:
            by_quadrant_count[index] += 1
    return by_quadrant_count


def print_grid(robots: dict[Coord, bool], max_dim: Coord):
    for y in range(max_dim.y):
        for x in range(max_dim.y):
            if Coord(x, y) in robots:
                print("X", end="")
            else:
                print(".", end="")
        print()


def group_neighbouring_robots(robots: dict[Coord, bool]) -> int:
    explored = {}
    group_count = 0
    for robot in robots.keys():
        if robot in explored:
            continue
        group_count += 1
        queue = [robot]
        while len(queue) > 0:
            curr_loc = queue.pop()
            explored[curr_loc] = True
            for dir in DIRECTIONS:
                next_coord = Coord(curr_loc.x + dir.x, curr_loc.y + dir.y)
                if (
                    next_coord in robots
                    and next_coord not in explored
                    and next_coord not in queue
                ):
                    queue.append(next_coord)

    return group_count


class Day14(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            grid_size = Coord(11, 7) if kwargs["test_mode"] else Coord(101, 103)
            robots = parse_input(file.readlines())
            moved_robots, _ = calc_robot_positions(robots, 100, grid_size)

            robots_by_quadrant = count_robots_in_quadrants(moved_robots, grid_size)
            print(math.prod(robots_by_quadrant))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            grid_size = Coord(11, 7) if kwargs["test_mode"] else Coord(101, 103)
            robots = parse_input(file.readlines())
            seconds = 0
            while True:
                robots, lookup = calc_robot_positions(robots, 1, grid_size)
                seconds += 1
                num_groups = group_neighbouring_robots(lookup)
                if num_groups / len(robots) < 0.5:
                    print_grid(lookup, grid_size)
                    print(group_neighbouring_robots(lookup), len(robots))
                    print(seconds)
                    input("Press Enter to continue...")
