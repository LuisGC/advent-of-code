from typing import List, Tuple

directions = {
    'U': (0, -1), # Up
    'R': (1, 0),  # Right
    'D': (0, 1),  # Down
    'L': (-1,0)   # Left
}

hex_int_to_dir = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}

def parse_input(lines: List[str]) -> List[Tuple[str, int]]:
    return [(line.split()[0], int(line.split()[1])) for line in lines]

def parse_input_hex(lines: List[str]) -> List[Tuple[str, int]]:
    hex_plan = []
    for line in lines:
        hex_part = line.split()[2]
        dir = hex_int_to_dir[hex_part[-2]]
        size = int(hex_part[2:-2], 16)
        hex_plan.append((dir, size))

    return hex_plan

def lava_capacity(dig_plan: List[str]) -> int:

    dig_plan = parse_input(dig_plan)

    trench = [(0, 0)]
    for dir, size in dig_plan:
        delta = directions[dir]
        for _ in range(size):
            trench.append((trench[-1][0] + delta[0], trench[-1][1] + delta[1]))

    trench_set = set(trench)

    # Filling from the outside
    min_x, min_y = trench[0]
    max_x, max_y = trench[0]

    for x, y in trench_set:
        min_y = min(min_y, y)
        min_x = min(min_x, x)
        max_y = max(max_y, y)
        max_x = max(max_x, x)

    outside_min_y = min_y - 1
    outside_min_x = min_x - 1
    outside_max_y = max_y + 1
    outside_max_x = max_x + 1

    seen = set()
    flood = [(outside_max_x, outside_min_y)]
    while flood:
        x, y = flood.pop()
        if (x, y) in seen:
            continue
        if (x, y) in trench_set:
            continue
        if (
            y < outside_min_y or
            y > outside_max_y or
            x < outside_min_x or
            x > outside_max_x
        ):
            continue

        seen.add((x, y))
        flood.append(((x    , y - 1)))
        flood.append(((x    , y + 1)))
        flood.append(((x - 1, y)))
        flood.append(((x + 1, y)))
    
    box_size = (outside_max_y - outside_min_y + 1) * (outside_max_x - outside_min_x + 1)
    enclosed = box_size - len(seen)

    return enclosed

def decode(color:str) -> Tuple:
    color = color[2:-1]
    distance = int(color[:5], 16)
    direction = hex_int_to_dir[color[-1]]
    return distance, direction

def move(x, y, direction, distance, area, position):
    delta_x, delta_y = directions[direction]
    new_x = x + delta_x * distance
    new_y = y + delta_y * distance
    area += (x + new_x) * (new_y - y)
    return new_x, new_y, area, position + distance

def shoelace(dig_plan: List[str], hex_mode: bool=False) -> int:
    x, y, area, position = 0, 0, 0, 0
    for line in dig_plan:
        direction, distance, color = line.split()
        distance = int(distance)
        if hex_mode:
            _, _, color = line.split()
            distance, direction = decode(color)

        x, y, area, position = move(x, y, direction, distance, area, position)

    return abs(area//2) + position//2 + 1


with open("2023/day-18/example.txt", encoding="utf-8") as f:
    dig_plan = [line.strip() for line in f.readlines()]

    assert 62 == lava_capacity(dig_plan)
    assert 62 == shoelace(dig_plan)    
    assert 952408144115 == shoelace(dig_plan, hex_mode=True)    

with open("2023/day-18/input.txt", encoding="utf-8") as f:
    dig_plan = [line.strip() for line in f.readlines()]
    
    print("Part 1: The amount of lava is ", lava_capacity(dig_plan))
    print("Part 2: The amount of lava in hex mode is ", shoelace(dig_plan, hex_mode=True))
