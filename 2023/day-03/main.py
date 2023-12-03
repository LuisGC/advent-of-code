from itertools import product
from typing import Tuple
from collections import defaultdict
from math import prod

def is_part(char: str) -> bool:
    return char not in ".0123456789"

def get_part_numbers(lines: list) -> Tuple[int,int]:
    total = 0
    all_gears = defaultdict(list)

    for i in range(len(lines)):
        initial_digit_pos = None
        near_part = False
        gears = set()

        for j in range(len(lines[i]) + 1):
            if j < len(lines[i]) and lines[i][j].isdigit():
                if initial_digit_pos is None:
                    initial_digit_pos = j

                for di, dj in product((-1, 0, 1), repeat=2):
                    si = i + di
                    sj = j + dj

                    if 0 <= si < len(lines) and 0 <= sj < len(lines[si]):
                        if is_part(lines[si][sj]):
                            near_part = True
                        if lines[si][sj] == "*":
                            gears.add((si, sj))
            else:
                if initial_digit_pos is not None:
                    number = int(lines[i][initial_digit_pos:j])
                    if near_part:
                        total += number
                    for gear in gears:
                        all_gears[gear].append(number)

                    initial_digit_pos = None
                    near_part = False
                    gears = set()

    return total, sum(prod(elts) for elts in all_gears.values() if len(elts) >= 2)


with open("2023/day-03/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total_part_numbers, sum_all_gear_ratios = get_part_numbers(input_lines)
    assert 4361 == total_part_numbers
    assert 467835 == sum_all_gear_ratios

with open("2023/day-03/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total_part_numbers, sum_all_gear_ratios = get_part_numbers(input_lines)
    print("Part 1: Sum of all part numbers is ", total_part_numbers)
    print("Part 2: Sum of all gear ratios is ", sum_all_gear_ratios)
