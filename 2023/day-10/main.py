from typing import List

MAZE_RULES = {
    ("L", 1j): 1, ("L", -1): -1j,
    ("J", 1j): -1, ("J", 1): -1j,
    ("7", 1): 1j, ("7", -1j): -1,
    ("F", -1): 1j, ("F", -1j): 1
}

def starting_position(input_lines: List[str]) -> complex:
    return [complex(j, i) for i, row in enumerate(input_lines) for j, char in enumerate(row) if char == "S"][0]

def distance(maze: List[str], start: complex, initial_direction: int = 1) -> int:
    dir = initial_direction

    pos = start + dir
    s = 1

    while pos != start:
        x, y = int(pos.real), int(pos.imag)
        if maze[y][x] not in ["|", "-"]:
            dir = MAZE_RULES[(maze[y][x], dir)]
        
        pos += dir
        s += 1

    return (s // 2)

with open("2023/day-10/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 4 == distance(input_lines, starting_position(input_lines))

with open("2023/day-10/example2.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 8 == distance(input_lines, starting_position(input_lines))
    
with open("2023/day-10/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    print("Part 1: The farthest distance is ", distance(input_lines, starting_position(input_lines), -1))
