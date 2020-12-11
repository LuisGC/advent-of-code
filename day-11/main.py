from typing import List
from collections import Counter
from typing import NamedTuple

class SeatingRules (NamedTuple):
    adjacent: bool
    neighbour_limit: int

Grid = List[List[str]]

def count_occupied (seat_layout: Grid) -> int:
    return sum(c == '#' for row in seat_layout for c in row)

neighbors = [(-1, 0), (-1, -1), (-1, +1),
             ( 0,-1),           ( 0, +1),
             ( 1, 1), (1,  0),  (1, - 1)]

def count_neighbours(seat_layout: Grid, row: int, col: int) -> str:
    rows = len(seat_layout)
    cols = len(seat_layout[0])

    occupied_neighbours = Counter(seat_layout[row + dr][col + dc]
        for dr, dc in neighbors
        if 0 <= row + dr < rows and 0 <= col + dc < cols)

    return occupied_neighbours["#"]

def next_value(seat_layout: Grid, row: int, col: int, rules: SeatingRules) -> str:
    seat_status = seat_layout[row][col]

    if rules.adjacent:
        neighbours = count_neighbours(seat_layout, row, col)

    if seat_status == 'L' and neighbours == 0:
        return '#'
    if seat_status == '#' and neighbours >= rules.neighbour_limit:
        return 'L'
    else:
        return seat_status

def apply_round(seat_layout: Grid, rules: SeatingRules) -> Grid:
    return [
        [
            next_value(seat_layout, i, j, rules)
            for j, col in enumerate(row)
        ]
        for i, row in enumerate(seat_layout)
    ]

def final_occupancy (seat_layout: Grid, rules: SeatingRules) -> int:

    while True:
        next_seat_layout = apply_round(seat_layout, rules)
        if next_seat_layout == seat_layout:
            break
        else:
            seat_layout = next_seat_layout

    return count_occupied(seat_layout)

with open("day-11/example.txt") as f:
    seat_layout = f.readlines()
    assert 37 == final_occupancy(seat_layout, SeatingRules(1,4))

with open("day-11/input.txt") as f:
    seat_layout = f.readlines()
    print("Part 1: The final occupancy is", final_occupancy(seat_layout, SeatingRules(1,4)))
