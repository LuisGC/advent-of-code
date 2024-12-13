from collections import defaultdict
from typing import Tuple
from itertools import permutations, count

def parse_input(lines: str) -> Tuple[set, defaultdict]:
    grid = {
        (row, col): char
        for row, line in enumerate(lines.split("\n"))
        for col, char in enumerate(line)
    }
    antennas = defaultdict(list)
    for pos, char in grid.items():
        if char != ".":
            antennas[char].append(pos)

    return set(grid), antennas

def find_antinodes(grid: set, antennas: defaultdict) -> set:
    return grid &  {
        (2 * row - row_other, 2 * col - col_other)
        for (row, col), (row_other, col_other) in permutations(antennas, r=2)
    }

def find_all_antinodes(grid: set, antennas: defaultdict) -> set:
    antinodes = set()
    for (row, col), (row_other, col_other) in permutations(antennas, r=2):
        dr, dc = row_other - row, col_other - col
        for n in count(1):
            if (antinode := (row + n * dr, col + n * dc)) not in grid:
                break
            antinodes.add(antinode)
    return antinodes

def unique_locations(grid: set, antennas: defaultdict, with_harmonics: bool = False) -> int:
    if with_harmonics:
        return len(set.union(*[find_all_antinodes(grid, pos) for pos in antennas.values()]))    
    else:
        return len(set.union(*[find_antinodes(grid, pos) for pos in antennas.values()]))


with open("2024/day-08/example.txt", encoding="utf-8") as f:
    grid, antennas = parse_input(f.read().rstrip())
    assert 14 == unique_locations(grid, antennas)
    assert 34 == unique_locations(grid, antennas, with_harmonics=True)

with open("2024/day-08/input.txt", encoding="utf-8") as f:
    grid, antennas = parse_input(f.read().rstrip())
    print(f"Part 1: Amount of unique locations is {unique_locations(grid, antennas)}")
    print(f"Part 2: Amount of unique locations with harmonics is {unique_locations(grid, antennas, with_harmonics=True)}")
