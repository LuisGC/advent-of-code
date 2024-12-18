import sys
import heapq
from typing import List, Tuple
sys.path.insert(0, './')
from utils import profiler, DIRECTIONS

EMPTY, CORRUPTED = ".#"

def parse_input(lines: List[str], memory_size: int, num_bytes: str) -> Tuple[List[List[str]], List[Tuple[int, int]]]:
    falling_bytes = []
    for line in lines:
        x, y = line.split(",")
        falling_bytes.append((int(x), int(y)))
    grid = [[EMPTY for _ in range(memory_size + 1)] for _ in range(memory_size + 1)]
    for i in range(min(num_bytes, len(lines))):
        x, y = falling_bytes[i]
        grid[y][x] = CORRUPTED

    return grid, falling_bytes

def shortest_path(grid: List[List[str]], memory_size: int) -> int:
    start = (0, 0)
    end = (memory_size, memory_size)

    queue = [(0, start)]
    visited = set()

    while queue:
        distance, location = heapq.heappop(queue)
        if location in visited:
            continue
        visited.add(location)
        if location == end:
            return distance
        
        for direction in DIRECTIONS:
            next_x, next_y = (location[0] + direction[0], location[1] + direction[1])
            if (0 <= next_x < memory_size + 1) and (0 <= next_y < memory_size + 1) and grid[next_y][next_x] != CORRUPTED:
                if (next_x, next_y) not in visited:
                    heapq.heappush(queue, (distance + 1, (next_x, next_y)))

@profiler
def first_blocking_byte(grid: List[List[str]], falling_bytes: List[Tuple[int, int]], memory_size: int, num_bytes: str) -> int:

    for i in range(num_bytes + 1, len(falling_bytes)):
        x, y = falling_bytes[i]
        grid[y][x] = CORRUPTED
        if shortest_path(grid, memory_size) is None:
            break
    return (x, y)


with open("2024/day-18/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    grid, falling_bytes = parse_input(input_lines, 6, 12)

    assert 22 == shortest_path(grid, 6)
    assert (6,1) == first_blocking_byte(grid, falling_bytes, 6, 12)

with open("2024/day-18/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    grid, falling_bytes = parse_input(input_lines, 70, 1024)

    print(f"Part 1: Minimum number of steps is {shortest_path(grid, 70)}")

    first = first_blocking_byte(grid, falling_bytes, 70, 1024)
    print(f"Part 2: Fist blocking byte is {",".join(map(str, first))}")