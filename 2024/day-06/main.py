import sys
import numpy as np
from typing import List
sys.path.insert(0, './')
from utils import DIRECTIONS, profiler

sys.setrecursionlimit(10**6)

def parse_input(input: str) -> List:
    data = []
    for line in input:
        data.append(list(line.strip()))
    data = np.array(data)
    return data
    
@profiler
def visited_positions(lines: List) -> int:
    direction = '^'
    map = []
    map = np.array(lines)

    row, col = np.argwhere(map == '^')[0]
    map[row][col] = 'X'

    while True:
        if direction == '^':
            if row - 1 < 0:
                map[row][col] = 'X'
                break
            elif map[row - 1][col] == "#":
                direction = ">"
            else:
                map[row][col] = 'X'
                row -= 1
        elif direction == '>':
            if col + 1 >= map.shape[1]:
                map[row][col] = 'X'
                break
            elif map[row][col + 1] == "#":
                direction = "v"
            else:
                map[row][col] = 'X'
                col += 1
        elif direction == 'v':
            if row + 1 >= map.shape[0]:
                map[row][col] = 'X'
                break
            elif map[row + 1][col] == "#":
                direction = "<"
            else:
                map[row][col] = 'X'
                row += 1
        elif direction == '<':
            if col - 1 < 0:
                map[row][col] = 'X'
                break
            elif map[row][col - 1] == "#":
                direction = "^"
            else:
                map[row][col] = 'X'
                col -= 1

    return np.count_nonzero(map == 'X')

with open("2024/day-06/example.txt", encoding="utf-8") as f:
    data = parse_input(f)
    assert 41 == visited_positions(data)

with open("2024/day-06/input.txt", encoding="utf-8") as f:
    data = parse_input(f)
    print(f"Part 1: Number of distinct positions visited is {visited_positions(data)}")
