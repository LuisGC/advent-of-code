import itertools
from typing import List
from collections import defaultdict

def parse_input(lines: List) -> set:
    elves = set()
    for y, line in enumerate(reversed(lines)):
        for x, char in enumerate(line):
            if char == "#":
                elves.add((x, y))
    return elves

def move_elves(elves: set, directions) -> int:
    proposed = defaultdict(list) # dest_coords: source_coords
    for col, row in elves:
        NE = (col + 1, row + 1) in elves
        N  = (col    , row + 1) in elves
        NW = (col - 1, row + 1) in elves
        E  = (col + 1, row    ) in elves
        W  = (col - 1, row    ) in elves
        SE = (col + 1, row - 1) in elves
        S  = (col    , row - 1) in elves
        SW = (col - 1, row - 1) in elves

        if not (NE or N or NW or W or E or SE or S or SW):
            continue

        for direction in directions:
            if direction == 'N' and not (NE or N or NW):
                proposed[(col, row+1)].append((col, row))
                break
            elif direction == 'S' and not (SE or S or SW):
                proposed[(col, row-1)].append((col, row))
                break
            elif direction == 'W' and not (NW or W or SW):
                proposed[(col-1, row)].append((col, row))
                break
            elif direction == 'E' and not (NE or E or SE):
                proposed[(col+1, row)].append((col, row))
                break

    for destination, source in proposed.items():
        if len(source) == 1:
            elves.remove(source[0])
            elves.add(destination)

    return len(proposed) > 0

def bounding_box(elves: set) -> tuple:
    elf_iter = iter(elves)
    x, y = next(elf_iter)
    min_x, min_y = x, y
    max_x, max_y = x, y
    for x, y in elf_iter:
        min_x, min_y = min(x, min_x), min(y, min_y)
        max_x, max_y = max(x, max_x), max(y, max_y)
    
    return max_x - min_x + 1, max_y - min_y + 1

def distribute_elves(elves: set, rounds: int) -> int:
    dir_prio = itertools.cycle('NSWE')
    for _ in range(rounds):
        move_elves(elves, list(itertools.islice(dir_prio, 4)))
        next(dir_prio)

    width, heigth = bounding_box(elves)
    return width * heigth - len(elves)

def finish_distributing(elves: set) -> int:
    dir_prio = itertools.cycle('NSWE')
    for round in itertools.count(1):
        if not move_elves(elves, list(itertools.islice(dir_prio, 4))):
            return round
        next(dir_prio)
    return -1

with open("2022/day-23/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    elves = parse_input(input_lines)
    assert 110 == distribute_elves(elves, 10)

    elves = parse_input(input_lines)
    assert 20 == finish_distributing(elves)

with open("2022/day-23/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    elves = parse_input(input_lines)
    print("Part 1: Empty ground tiles are:", distribute_elves(elves, 10))
    
    elves = parse_input(input_lines)
    print("Part 2: Rounds until elves are distributed are:", finish_distributing(elves))
