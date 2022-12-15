from typing import List, Tuple
from functools import reduce
import re

def manhatan(coord_a: tuple, coord_b: tuple) -> int:
    return abs(coord_a[0]-coord_b[0]) + abs(coord_a[1]-coord_b[1])

def parse_input(lines: List) -> List:
    items = []
    for line in lines:
        chunks = re.split(',|=|:', line)
        sensor, beacon = (int(chunks[1]), int(chunks[3])), (int(chunks[5]), (int(chunks[7])))
        item = {
            "sensor" : sensor,
            "beacon" : beacon,
            "distance" : manhatan(sensor, beacon)
        }
        items.append(item)

    return items

def analyze_row(items: List, max: float, row: int) -> List:

    impossible_ranges = []
    for item in items:
        s_x, s_y = item['sensor']

        offset = item['distance'] - abs(s_y - row)
        if offset < 0: continue

        lowest_x, highest_x = s_x - offset, s_x + offset
        impossible_ranges.append((lowest_x, highest_x))

    return impossible_ranges

def merge_ranges(ranges):
    merged_ranges = []
    for start, end in sorted(ranges):

        if len(merged_ranges) == 0:
            merged_ranges.append([start,end])
            continue

        _,q_end = merged_ranges[-1]

        if start > q_end:
            merged_ranges.append([start,q_end])
            continue

        merged_ranges[-1][1] = max(q_end,end)
   
    return merged_ranges

def positions_without_beacon(items: List, row: int) -> int:

    occupied = set()
    impossible_ranges = analyze_row(items, float("inf"), row)
    for item in items:
        b_x, b_y = item['beacon']
        if b_y == row:
            occupied.add(b_x)
    merged_ranges = merge_ranges(impossible_ranges)

    return abs(merged_ranges[0][1] - merged_ranges[0][0]) - len(occupied) + 1

with open("2022/day-15/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    items = parse_input(input_lines)
    
    assert 26 == positions_without_beacon(items, 10)

with open("2022/day-15/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    items = parse_input(input_lines)
    
    print("Part 1: Positions without beacon in line 10 are:", positions_without_beacon(items, 2000000))
