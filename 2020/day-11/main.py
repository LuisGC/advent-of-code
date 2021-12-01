from typing import List
from collections import Counter
from typing import NamedTuple


class SeatingRules (NamedTuple):
    adjacent: bool
    neighbour_limit: int


Grid = List[List[str]]

neighbors = [(-1, 0), (-1, -1), (-1, +1),
             ( 0,-1),           ( 0, +1),
             ( 1, 1), (1,  0),  (1, - 1)]


def count_adjacent_neighbours(seat_layout: Grid, row: int, col: int) -> str:
    num_rows = len(seat_layout)
    num_cols = len(seat_layout[0])

    occupied_neighbours = Counter(
        seat_layout[row + dr][col + dc]
        for dr, dc in neighbors
        if 0 <= row + dr < num_rows and 0 <= col + dc < num_cols)

    return occupied_neighbours["#"]


def first_occupied(seat_layout: Grid, row: int, col: int, dr: int,
                   dc: int) -> str:

    num_rows = len(seat_layout)
    num_cols = len(seat_layout[0])

    while True:
        row += dr
        col += dc

        if 0 <= row < num_rows and 0 <= col < num_cols:
            c = seat_layout[row][col]
            if c == '#' or c == 'L':
                return c
        else:
            return '.'


def count_visible_neighbours(seat_layout: Grid, row: int, col: int) -> str:
    occupied_neighbours = Counter(first_occupied(seat_layout, row, col, dr, dc)
                                  for dr, dc in neighbors)

    return occupied_neighbours["#"]


def next_value(seat_layout: Grid, row: int, col: int,
               rules: SeatingRules) -> str:
    seat_status = seat_layout[row][col]

    if rules.adjacent:
        neighbours = count_adjacent_neighbours(seat_layout, row, col)
    else:
        neighbours = count_visible_neighbours(seat_layout, row, col)

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


def count_occupied(seat_layout: Grid) -> int:
    return sum(c == '#' for row in seat_layout for c in row)


def final_occupancy(seat_layout: Grid, rules: SeatingRules) -> int:

    while True:
        next_seat_layout = apply_round(seat_layout, rules)
        if next_seat_layout == seat_layout:
            break
        else:
            seat_layout = next_seat_layout

    return count_occupied(seat_layout)


with open("day-11/example.txt") as f:
    seat_layout = f.readlines()
    assert 37 == final_occupancy(seat_layout, SeatingRules(1, 4))
    assert 26 == final_occupancy(seat_layout, SeatingRules(0, 5))


with open("day-11/input.txt") as f:
    seat_layout = f.readlines()
    print("Part 1: The final occupancy is",
          final_occupancy(seat_layout, SeatingRules(1, 4)))
    print("Part 2: The final occupancy with the new rules is",
          final_occupancy(seat_layout, SeatingRules(0, 5)))
