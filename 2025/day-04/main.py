import sys
sys.path.insert(0, './')
from utils import DIRECTIONS_ALL

def accessible_rolls(lines: list[list[str]], removing: bool = False) -> int:
    rolls = 0

    removed = True
    while removed:
        removed = False

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                count = 0
                if lines[i][j] != "@":
                    continue

                for di, dj in DIRECTIONS_ALL:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < len(lines) and 0 <= nj < len(lines[i]):
                        if lines[ni][nj] == "@":
                            count += 1
                if count < 4:
                    rolls += 1
                    if removing:
                        lines[i][j] = "."
                        removed = True
    
    return rolls

with open("2025/day-04/example.txt", encoding="utf-8") as f:
    input_lines = [list(line) for line in f.readlines()]
    assert 13 == accessible_rolls(input_lines)
    assert 43 == accessible_rolls(input_lines, removing=True)

with open("2025/day-04/input.txt", encoding="utf-8") as f:
    input_lines = [list(line) for line in f.readlines()]

    print(f"Part 1: The amount of accessible rolls is {accessible_rolls(input_lines)}")
    print(f"Part 2: The amount of accessible rolls removing is {accessible_rolls(input_lines, removing=True)}")
