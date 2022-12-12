from typing import List, Tuple
from collections import deque

def parse_input(lines: List[str]) -> Tuple:
    heightmap = []
    start = None
    end = None
    possible_starts = []

    for col, line in enumerate(lines):
        heightmap.append([])
        for row, position in enumerate(line.strip()):
            if position == "S":
                start = (row, col)
                heightmap[-1].append(0)
            elif position == "E":
                end = (row, col)
                heightmap[-1].append(ord('z')-ord('a'))
            elif position == "a":
                possible_starts.append((row, col))
                heightmap[-1].append(0)
            else:
                heightmap[-1].append(ord(position)-ord('a'))

    # print("\n".join(map(str, heightmap)))
    return heightmap, start, end, possible_starts

def next_steps(heightmap, position) -> List:
    options = []
    for (x, y) in [(0,-1), (0, 1), (1, 0), (-1, 0)]:
        new_position = (position[0] + x, position[1] + y)
        if new_position[0] < 0 or new_position[1] < 0 or new_position[0] >= len(heightmap[0]) or new_position[1] >= len(heightmap):
            continue
        if heightmap[position[1] + y][position[0] + x] <= heightmap[position[1]][position[0]] + 1:
            options.append(new_position)
            
    return options

def count_steps(heightmap, start, end) -> int:
    to_explore = deque()
    to_explore.extend([start, x] for x in next_steps(heightmap, start))
    visited = set()
    while len(to_explore):
        path = to_explore.popleft()
        steps = next_steps(heightmap, path[-1])
        for step in steps:
            if step == end:
                return(len(path))
            if step not in visited:
                visited.add(step)
                to_explore.append(path + [step])
    return -1

def shortest_route(heightmap, possible_starts, end) -> int:
    shortest_route = -1
    for start in possible_starts:
        steps = count_steps(heightmap, start, end)
        if steps != -1 and (steps < shortest_route or shortest_route == -1):
            shortest_route = steps

    return shortest_route

with open("2022/day-12/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    heightmap, start, end, possible_starts = parse_input(input_lines)
    assert 31 == count_steps(heightmap, start, end)
    assert 29 == shortest_route(heightmap, possible_starts, end)

with open("2022/day-12/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    heightmap, start, end, possible_starts = parse_input(input_lines)

    print("Part 1: Count of visited positions:", count_steps(heightmap, start, end))
    print("Part 2: Shortes route is:", shortest_route(heightmap, possible_starts, end))
