from typing import List
from collections import defaultdict, deque

directions = {
    0: (0, -1), # N
    1: (1, 0),  # E
    2: (0, 1),  # S
    3: (-1,0)   # W
}

def is_valid(grid: List[str], x: int, y: int, infinite_garden: bool) -> bool:
    width = len(grid[0])
    heigth = len(grid)

    if not infinite_garden and not 0 <= x < width:
        return False
    if not infinite_garden and not 0 <= y < heigth:
        return False
    if infinite_garden:
        x %= width
        y %= heigth

    return grid[y][x] in ".S"

def walk_garden(grid: List[str], steps: int, infinite_garden: bool = False) -> int:
    width = len(grid[0])
    heigth = len(grid)

    seen = set()
    garden = defaultdict(set)
    queue = deque()

    for y in range(heigth):
        for x in range(width):
            if grid[y][x] == "S":
                queue.append((x, y, steps))

    while len(queue) > 0:
        x, y, step = queue.popleft()

        if (x, y, step) in seen:
            continue
        seen.add((x, y, step))

        if step == 0:
            continue

        for deltax, deltay in directions.values():
            new_x = x + deltax
            new_y = y + deltay
            if not is_valid(grid, new_x, new_y, infinite_garden):
                continue
            queue.append((new_x, new_y, step - 1))

    return sum(1 for v in seen if v[2] == 0)

def estimate_walking(grid: List[str]) -> int:
    return 0

with open("2023/day-21/example.txt", encoding="utf-8") as f:
    grid = [list(line.strip()) for line in f.readlines()]

    assert 16 == walk_garden(grid, 6)
    assert 16 == walk_garden(grid, 6, infinite_garden=True)
    assert 50 == walk_garden(grid, 10, infinite_garden=True)
    assert 1594 == walk_garden(grid, 50, infinite_garden=True)
    # assert 6536 == walk_garden(grid, 100, infinite_garden=True)
    # assert 167004 == walk_garden(grid, 500, infinite_garden=True)
    # assert 668697 == walk_garden(grid, 1000, infinite_garden=True)
    # assert 16733044 == walk_garden(grid, 5000, infinite_garden=True)

with open("2023/day-21/input.txt", encoding="utf-8") as f:
    grid = [list(line.strip()) for line in f.readlines()]
    
    print("Part 1: The garden plots that can be reached are ", walk_garden(grid, 64))
    # print("Part 2: The garden plots that can be reached with an infinite garden are ", walk_garden(grid, steps=26501365, infinite_garden=True))
