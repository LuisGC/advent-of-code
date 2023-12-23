from typing import List
from collections import defaultdict

DIRECTIONS = {
    0: ( 0, -1),  # W
    1: ( 1,  0),  # S
    2: ( 0,  1),  # E
    3: (-1,  0)   # N
}

def longest_hike(input_lines: List[str]) -> int:

    memo = defaultdict(lambda: -1)

    queue = [((0, 1), set(), 0)] # position, visited, steps

    while queue:
        current, queue = queue[0], queue[1:]
        position, visited, steps = current

        memo[position] = steps
        row, col = position

        dirs = [dir for dir in DIRECTIONS.values()]

        if input_lines[row][col] == ">":
            dirs = [DIRECTIONS[2]]
        elif input_lines[row][col] == "<":
            dirs = [DIRECTIONS[0]]
        elif input_lines[row][col] == "^":
            dirs = [DIRECTIONS[3]]
        elif input_lines[row][col] == "v":
            dirs = [DIRECTIONS[1]]
        
        for new_dir in dirs:
            new_row = position[0] + new_dir[0]
            new_col = position[1] + new_dir[1]
            new_pos = (new_row, new_col)
            if (new_pos not in visited and
                0 <= new_row < len(input_lines) and 0 <= new_col < len(input_lines[0]) and
                input_lines[new_row][new_col] != "#" and
                memo[position] < steps + 1):
                queue.append((new_pos, visited | {position}, steps + 1))

    return memo[((len(input_lines)-1), len(input_lines[-1])-2)]

with open("2023/day-23/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    
    assert 94 == longest_hike(input_lines)

with open("2023/day-23/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    
    print("Part 1: The longest hike is ", longest_hike(input_lines))