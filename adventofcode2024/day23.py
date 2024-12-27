from itertools import combinations

from common import AdventSolution


def parse_graph(input: list[str]) -> dict[str, dict[bool]]:
    graph = {}
    for line in input:
        val = line.strip().split("-")
        if val[0] not in graph:
            graph[val[0]] = {}
        if val[1] not in graph:
            graph[val[1]] = {}
        graph[val[0]][val[1]] = True
        graph[val[1]][val[0]] = True
    return graph


def find_3cliques_beginning_with(
    graph: dict[str, dict[bool]], prefix: str | None
) -> set[tuple]:
    found = set()
    for start in graph.keys():
        if prefix and not start.startswith(prefix):
            continue
        for left, right in combinations(graph.keys(), 2):
            if left == start or right == start:
                continue
            if start in graph[left] and start in graph[right] and left in graph[right]:
                found.add(tuple(sorted([start, left, right])))
    return found


def grow_cliques(graph: dict[str, dict[bool]], prev_cliques: set[tuple]) -> set[tuple]:
    found = set()
    explored = {}
    for clique in prev_cliques:
        for v in graph.keys():
            if v in clique:
                continue
            vals = [c for c in clique] + [v]
            key = tuple(sorted(vals))
            if key in explored:
                continue
            explored[key] = True
            all_connected = True
            for c in clique:
                if c not in graph[v]:
                    all_connected = False
                    break
            if all_connected:
                found.add(key)
    return found


class Day23(AdventSolution):
    @classmethod
    def part_one(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            graph = parse_graph(file.readlines())
            sets = find_3cliques_beginning_with(graph, "t")
            print(len(sets))

    def part_two(self, input_file: str, **kwargs):
        with open(input_file, "r") as file:
            graph = parse_graph(file.readlines())
            sets = find_3cliques_beginning_with(graph, None)
            iter = 3
            while len(sets) > 0:
                print(f"#{iter} cliques", len(sets))
                if len(sets) == 1:
                    for s in sets:
                        print(",".join(v for v in s))
                sets = grow_cliques(graph, sets)
                iter += 1
