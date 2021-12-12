from typing import List
from collections import defaultdict


def count_possible_paths(cave_routes: defaultdict, current_path: List[str]) -> int:
    current_cave = current_path[-1]
    if current_cave == 'end':
        return 1
    if current_cave.islower() and current_cave in current_path[:-1]:
        return 0

    next_caves = cave_routes[current_path[-1]]
    return sum([count_possible_paths(cave_routes, current_path + [cave]) for cave in next_caves])


def parse_input(input: List[str]) -> defaultdict:
    cave_routes = defaultdict(list)

    for route in input:
        start, end = route.split("-")
        cave_routes[start].append(end)
        cave_routes[end].append(start)

    return cave_routes


with open("2021/day-12/example.txt") as f:
    cave_routes = parse_input([line.strip() for line in f])
    assert 10 == count_possible_paths(cave_routes, ['start'])

with open("2021/day-12/example-2.txt") as f:
    cave_routes = parse_input([line.strip() for line in f])
    assert 19 == count_possible_paths(cave_routes, ['start'])

with open("2021/day-12/example-3.txt") as f:
    cave_routes = parse_input([line.strip() for line in f])
    assert 226 == count_possible_paths(cave_routes, ['start'])

with open("2021/day-12/input.txt") as f:
    cave_routes = parse_input([line.strip() for line in f])
    print("Part 1: The total possible paths is : ", count_possible_paths(cave_routes, ['start']))
#     print("Part 2: First synchronous flash is after (days): ", first_synchronous_flash(octopuses))
