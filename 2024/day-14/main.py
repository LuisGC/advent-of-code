import sys
from typing import List, Tuple
from statistics import stdev, mean
sys.path.insert(0, './')
from utils import profiler, DIRECTIONS

sys.setrecursionlimit(10**6)

def parse_robot(line: str) -> Tuple[int, int, int, int]:
    left, right = line.split()
    pos_x, pos_y = map(int, left[2:].split(","))
    vel_x, vel_y = map(int, right[2:].split(","))
    return (pos_x, pos_y, vel_x, vel_y)

def calculate_position(robot: Tuple[int, int, int, int], width: int, height: int, time: int) -> Tuple[int, int]:
    x, y, dx, dy = robot
    return (x + dx * time) % width, (y + dy * time) % height

@profiler
def get_safety_factor(robots: List[Tuple[int, int, int, int]], width: int, height: int, time: int) -> int:
    positions = [calculate_position(robot, width, height, time) for robot in robots]

    limit_x, limit_y = (width -1) / 2, (height - 1) / 2

    top_left = sum(1 for x, y in positions if x < limit_x and y < limit_y)
    top_right = sum(1 for x, y in positions if x > limit_x and y < limit_y)
    bottom_left = sum(1 for x, y in positions if x < limit_x and y > limit_y)
    bottom_right = sum(1 for x, y in positions if x > limit_x and y > limit_y)

    return top_left * top_right * bottom_left * bottom_right

@profiler
def find_tree(robots: List[Tuple[int, int, int, int]], width: int, height: int) -> int:
    time = 1
    cycle_time = 1
    iterations = []

    while True:
        positions = [calculate_position(robot, width, height, time) for robot in robots]
        x_coords = [x for x,_ in positions]
        y_coords = [y for _, y in positions]

        if cycle_time == 1: # horizontal clustering
            cluster_value = stdev(x_coords)
        else: # vertical clustering
            cluster_value = stdev(y_coords)

        iterations.append(cluster_value)
        mean_cluster = mean(iterations)

        if cluster_value < mean_cluster * 0.8:
            if cycle_time == 1:
                print(f"found horizontal clustering at time {time}")
                iterations = [stdev(y_coords)] #reset the vertical phase
                cycle_time = width
            else:
                print(f"found complete pattern at time {time}")
                return time

        if time > 100000:
            return -1
        
        time += cycle_time

with open("2024/day-14/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    robots = [parse_robot(line) for line in input_lines]

    assert 12 == get_safety_factor(robots, 11, 7, 100)

with open("2024/day-14/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    robots = [parse_robot(line) for line in input_lines]

    print(f"Part 1: Safety Factor is {get_safety_factor(robots, 101, 103, 100)}")
    print(f"Part 2: XMas tree is found after this time: {find_tree(robots, 101, 103)}")
    