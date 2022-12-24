from typing import List

DIRECTIONS = {
    '.': 0,
    '>': 2,
    'v': 8,
    '<': 1,
    '^': 4
}

def parse_input(lines: List) -> List:
    valley = []
    for line in lines:
        line = list(line)
        for index, char in enumerate(line):
            if char in DIRECTIONS:
                line[index] = DIRECTIONS[char]
        valley.append(line)
    return valley

def move_blizzards(valley: List) -> List:
    heigth = len(valley) - 2
    width = len(valley[0]) - 2
    new_valley = []
    new_valley.append(list(valley[0])) # first line does not change
    for _ in range(heigth):
        new_valley.append(['#'] + [0 for _ in range(width)] + ['#'])
    new_valley.append(list(valley[-1])) # last line does not change

    for row in range(1, heigth + 1):
        for col in range(1, width + 1):
            if valley[row][col] & 1:
                new_valley[row][(col - 2) % width + 1] |= 1
            if valley[row][col] & 2:
                new_valley[row][col % width + 1] |= 2
            if valley[row][col] & 4:
                new_valley[(row - 2) % heigth + 1][col] |= 4
            if valley[row][col] & 8:
                new_valley[row % heigth + 1][col] |= 8

    return new_valley

def walk(valley: List, start: tuple, goal: tuple, steps: int=0) -> int:
    locations = set()
    locations.add(start)

    while True:
        if goal in locations:
            return steps
        steps += 1
        valley = move_blizzards(valley)
        next_locations = set()
        for row, col in locations:
            if valley[row][col] == 0:
                next_locations.add((row, col))
            if row - 1 >= 0 and valley[row - 1][col] == 0:
                next_locations.add((row - 1, col))
            if row + 1 >= 0 and valley[row + 1][col] == 0:
                next_locations.add((row + 1, col))
            if valley[row][col - 1] == 0:
                next_locations.add((row, col - 1))
            if valley[row][col + 1] == 0:
                next_locations.add((row, col + 1))
        locations = next_locations

def steps_to_cross_valley(valley: List) -> int:
    start = (0,1)
    goal = (len(valley) - 1, len(valley[-1]) - 2)

    steps = walk(valley, start, goal, 0)
    return steps

with open("2022/day-24/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    valley = parse_input(input_lines)

    assert 18 == steps_to_cross_valley(valley)

with open("2022/day-24/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    valley = parse_input(input_lines)

    print("Part 1: Steps to cross the valley are:", steps_to_cross_valley(valley))
