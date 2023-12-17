from typing import List
from heapq import heappop, heappush

directions = {
    0: (0, -1), # N
    1: (1, 0),  # E
    2: (0, 1),  # S
    3: (-1,0)   # W
}

def min_heat_loss(city_map: List, min_distance: int, max_distance: int) -> int:
    heap = [(0, 0, 0, -1)] # loss, row, col, direction
    seen = set()
    losses = {}
    heigth = len(city_map)
    width = len(city_map[0])

    while heap:
        loss, row, col, direction = heappop(heap)
        if (row == heigth - 1) and (col == width - 1): # Final location
            return loss
        
        if (row, col, direction) not in seen:
            seen.add((row, col, direction))
            for new_direction in range(4):
                additional_loss = 0
                if direction == new_direction or (new_direction + 2) % 4 == direction:
                    continue

                for distance in range(1, max_distance + 1):
                    new_row = row + directions[new_direction][0] * distance
                    new_col = col + directions[new_direction][1] * distance
                    if not (0 <= new_row < heigth and 0 <= new_col < width):
                        break
                    additional_loss += int(city_map[new_row][new_col])
                    if distance >= min_distance:
                        new_loss = loss + additional_loss

                        if losses.get((new_row, new_col, new_direction), float("inf")) > new_loss:
                            losses[(new_row, new_col, new_direction)] = new_loss
                            heappush(heap, (new_loss, new_row, new_col, new_direction))


with open("2023/day-17/example.txt", encoding="utf-8") as f:
    city_map = [list(line.strip()) for line in f.readlines()]

    assert 102 == min_heat_loss(city_map, 1, 3)
    assert 94 == min_heat_loss(city_map, 4, 10)

with open("2023/day-17/input.txt", encoding="utf-8") as f:
    city_map = [list(line.strip()) for line in f.readlines()]
    
    print("Part 1: The minimum heat loss is ", min_heat_loss(city_map, 1, 3))
    print("Part 2: The minimum heat loss with ultra crucible is ", min_heat_loss(city_map, 4, 10))    