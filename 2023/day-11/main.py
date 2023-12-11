from typing import List, Tuple
from math import comb

def get_locations(map: List[str]) -> List[Tuple[int, int]]:
    return [
        (x, y)
        for y, row in enumerate(map)
        for x, char in enumerate(row)
        if char == "#"
    ]

def unocuppied_space(map: List[str], galaxies: List[Tuple]) -> Tuple[List[int], List[int]]:
    empty_x = [
        x for x in range(len(map[0]))
        if x not in [gx for gx,_ in galaxies]
    ]
    empty_y = [
            y for y in range(len(map))
            if y not in [gy for _,gy in galaxies]
    ]
    return empty_x, empty_y

def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return sum(abs(b[i] - a[i]) for i in range(len(a)))

def is_between(a: int, b: int, x: int) -> bool:
    return min(a, b) < x < max(a, b)

def galaxies_distance(a: Tuple[int, int], b: Tuple[int, int], unocuppied: Tuple[List, List], gap_offset: int) -> List[int]:
    def offset(axis: str) -> int:
        return sum(
            (gap_offset - 1) if is_between(a[axis == "y"], b[axis == "y"], gap) else 0
            for gap in unocuppied[axis == "y"]
        )
    return manhattan_distance(a, b) + offset("x") + offset("y")

def calculate_distances(map: List[str], gap_offset: int = 2) -> int:
    galaxies = get_locations(map)
    connections = [
        (a, b)
        for a in range(len(galaxies))
        for b in range(a, len(galaxies))
        if a != b
    ]
    assert comb(len(galaxies), 2) == len(connections)

    unocuppied = unocuppied_space(map, galaxies)

    distances = {
        (a, b): galaxies_distance(galaxies[a], galaxies[b], unocuppied, gap_offset)
        for a, b in connections
    }

    return distances.values()

with open("2023/day-11/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 374 == sum(calculate_distances(input_lines))
    assert 1030 == sum(calculate_distances(input_lines, 10))
    assert 8410 == sum(calculate_distances(input_lines, 100))

with open("2023/day-11/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    
    print("Part 1: Sum of distance of all galaxies is ", sum(calculate_distances(input_lines)))
    print("Part 1: Sum of distance of all galaxies if much older is ", sum(calculate_distances(input_lines, 1000000)))
