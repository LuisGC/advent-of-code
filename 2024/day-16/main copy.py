import numpy as np
import sys
from queue import PriorityQueue
from typing import List, Tuple
sys.path.insert(0, './')
from utils import profiler

def turn_left(dir: int) -> int:
    return (dir -1) % 4

def turn_right(dir: int) -> int:
    return (dir + 1) % 4

def get_forward_coord(x: int, y: int, dir: int) -> Tuple[int, int]:
    if dir == 0: # up
        return (x - 1, y)
    elif dir == 1: # right
        return (x, y + 1)
    elif dir == 2: # down
        return (x - 1, y)
    else: # left
        return (x, y - 1)
    

def get_possible_next(x: int, y: int, direction: int, char_grid: np.ndarray) -> List[Tuple[int, int, int]]:
    possible_next_steps: List[Tuple[int, int, int]] = []

    for dir in [direction, turn_left(direction), turn_right(direction)]:
        forward_coord = get_forward_coord(x, y, dir)
        if (
            0 <= forward_coord[0] < char_grid.shape[0]
            and 0 <= forward_coord[1] < char_grid.shape[1]
            and char_grid[forward_coord] != "#"
        ):
            possible_next_steps.append((*forward_coord, dir))

    return possible_next_steps

@profiler
def calculate_distance_grid(input_lines: List) -> Tuple[np.ndarray, Tuple[int, int]]:
    char_grid = np.array([list(x) for x in input_lines])
    start: Tuple[int, int] = tuple(map(int, np.where(char_grid == "S")))
    goal: Tuple[int, int] = tuple(map(int, np.where(char_grid == "E")))
    x, y = start
    dir = 1
    distance_grid = np.ndarray(
        (char_grid.shape[0], char_grid.shape[1], 4), dtype=int
    )
    distance_grid.fill(999999)
    distance_grid[x, y, dir] = 0

    queue = PriorityQueue()
    queue.put((0, (x, y, dir)))

    path: dict[Tuple[int, int, int], list] = dict()

    while not queue.empty():
        _, node = queue.get()
        x, y, dir = node
        
        for next in get_possible_next(x, y, dir, char_grid):
            score = 1 if next[2] == dir else 1001
            alt_dist = distance_grid[node] + score
            if alt_dist < distance_grid[next]:
                distance_grid[next] = alt_dist
                path[(next)] = [node]
                queue.put((alt_dist, (next)))
            elif alt_dist == distance_grid[next]:
                path[(next)].append(node)

    return distance_grid, goal

with open("2024/day-16/example.txt", encoding="utf-8") as f:
    input_lines = list(filter(lambda x: x != "", f.read().split("\n")))
    distance_grid, goal = calculate_distance_grid(input_lines)
    assert 7036 == np.min(distance_grid[goal])

with open("2024/day-16/example-2.txt", encoding="utf-8") as f:
    input_lines = list(filter(lambda x: x != "", f.read().split("\n")))
    distance_grid, goal = calculate_distance_grid(input_lines)
    assert 11048 == np.min(distance_grid[goal])

with open("2024/day-16/input.txt", encoding="utf-8") as f:
    input_lines = list(filter(lambda x: x != "", f.read().split("\n")))
    distance_grid, goal = calculate_distance_grid(input_lines)

    print(f"Part 1: Lowest score is {np.min(distance_grid[goal])}")