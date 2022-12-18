import numpy as np
from typing import List

NEIGHBORS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]

def parse_lines(lines: List) -> set:
    positions = set()
    for row in lines:
        x, y, z = map(int, row.split(','))
        positions.add((x, y, z))

    return positions

def surface_area(positions: set) -> int:
    surface_area = 0

    for x, y, z in positions:
        for dx, dy, dz in NEIGHBORS:
            if (x + dx, y + dy, z + dz) not in positions:
                surface_area += 1

    return surface_area

def is_contained(x: int, y: int, z: int, max: int) -> bool:
    return x >= 0 and y >= 0 and z >= 0 and x <= max and y <= max and z <= max

def exterior_surface_area(positions: set) -> int:
    surface_area = 0

    max_dimension = 0
    for x, y, z in positions:
        max_dimension = max(max_dimension, x, y, z)

    matrix = np.zeros((max_dimension + 1, max_dimension + 1, max_dimension + 1), dtype = int)

    # lava drops will be 1s
    for x, y, z in positions:
        matrix[(x, y, z)] = 1

    # positions with water will be 2s
    queue = [(0, 0, 0)]
    matrix[(0, 0, 0)] = 2

    while queue:
        x, y, z = queue.pop()
        for dx, dy, dz in NEIGHBORS:
            if is_contained(x + dx, y + dy, z + dz, max_dimension) and matrix[(x + dx, y + dy, z + dz)] == 0:
                queue.append((x + dx, y + dy, z + dz))
                matrix[(x + dx, y + dy, z + dz)] = 2

    for x in range(max_dimension + 1):
        for y in range(max_dimension + 1):
            for z in range(max_dimension + 1):
                if matrix[(x, y, z)] == 1:
                    for dx, dy, dz in NEIGHBORS:
                        if not is_contained(x + dx, y + dy, z + dz, max_dimension) or matrix[(x + dx, y + dy, z + dz)] == 2:
                            surface_area += 1

    return surface_area

with open("2022/day-18/example.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines()]
    positions = parse_lines(lines)

    assert 10 == surface_area({(1, 1, 1), (2, 1, 1)})
    assert 64 == surface_area(positions)
    assert 58 == exterior_surface_area(positions)

with open("2022/day-18/input.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines()]
    positions = parse_lines(lines)

    print("Part 1: Surface area of lava is:", surface_area(positions))
    print("Part 2: Exterior Surface area of lava is:", exterior_surface_area(positions))
