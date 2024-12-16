import sys
from typing import List, Tuple
sys.path.insert(0, './')
from utils import arrow_dir, profiler

sys.setrecursionlimit(10**6)

def find_guard(map_data: List[str]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            if cell in arrow_dir:
                return (i, j), arrow_dir[cell]
            
    return None, None

def simulate_guard(map_data: List[str], start_pos: Tuple[int, int], start_dir: Tuple[int, int]) -> Tuple[int, bool]:
    visited = set()
    pos = start_pos
    direction = start_dir
    rows, cols = len(map_data), len(map_data[0])

    i = 0
    while i < rows * cols * 4:
        visited.add(pos)
        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if next_pos[0] < 0 or rows <= next_pos[0] or next_pos[1] < 0 or cols <= next_pos[1]:
            return visited, False
        if 0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols and map_data[next_pos[0]][next_pos[1]] != "#":
            pos = next_pos
        else:
            direction = (direction[1], -direction[0])
        i += 1
    
    return visited, True

def simulate_guard_with_obstruction(map_data: List[str], start_pos: Tuple[int, int], start_dir: Tuple[int, int], obstruction_pos: Tuple[int, int]) -> bool:
    map_data[obstruction_pos[0]][obstruction_pos[1]] = '#'
    _, loop_detected = simulate_guard(map_data, start_pos, start_dir)
    map_data[obstruction_pos[0]][obstruction_pos[1]] = '.' # Reset the position
    return loop_detected

@profiler
def valid_obstruction_positions(map_data: List[str], visited_positions: set, start_pos: Tuple[int, int], start_dir: Tuple[int, int]) -> int:
    valid_obstruction_positions = 0
    for pos in visited_positions:
        if pos == start_pos:
            continue
        if simulate_guard_with_obstruction(map_data, start_pos, start_dir, pos):
            valid_obstruction_positions += 1

    return valid_obstruction_positions


with open("2024/day-06/example.txt", encoding="utf-8") as f:
    map_data = [list(line.strip()) for line in f]
    start_pos, start_dir = find_guard(map_data)
    visited_positions, _ = simulate_guard(map_data, start_pos, start_dir)

    assert 41 == len(visited_positions)
    assert 6 == valid_obstruction_positions(map_data, visited_positions, start_pos, start_dir)

with open("2024/day-06/input.txt", encoding="utf-8") as f:
    map_data = [list(line.strip()) for line in f]
    start_pos, start_dir = find_guard(map_data)
    visited_positions, _ = simulate_guard(map_data, start_pos, start_dir)

    print(f"Part 1: Number of distinct positions visited is {len(visited_positions)}")
    print(f"Part 2: Number of valid obstruction positions is {valid_obstruction_positions(map_data, visited_positions, start_pos, start_dir)}")
