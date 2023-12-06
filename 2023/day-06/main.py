from math import prod
from typing import List, Tuple

def parse_input (lines: List[str]) -> Tuple[List[int], List[int]]:
    times = []
    distances = []
    for item in lines[0].split()[1:]:
        times.append(int(item))
    for item in lines[1].split()[1:]:
        distances.append(int(item))

    return times, distances

def parse_input_kerning(lines: List[str]) -> Tuple[List[int], List[int]]:
    times = ''
    distances = ''
    for item in lines[0].split()[1:]:
        times += item
    for item in lines[1].split()[1:]:
        distances += item
    return [int(times)], [int(distances)]

def distance_travelled(max_time: int, button_holding_time: int) -> int:
    distance = (max_time - button_holding_time) * button_holding_time
    return distance

def beat_record(time: int, distance: int) -> int:
    records = 0

    for i in range(1, time):
        if distance_travelled(time, i) > distance:
            records += 1
    return records

def record_options(times: List[int], distances: List[int]) -> List[int]:
    total_records = []

    for i in range(len(times)):
        records = beat_record(times[i], distances[i])
        total_records.append(records)

    return total_records

with open("2023/day-06/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    times, distances = parse_input(input_lines)
    assert 288 == prod(record_options(times, distances))
    
    times, distances = parse_input_kerning(input_lines)
    assert 71503 == record_options(times, distances)[0]


with open("2023/day-06/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    
    times, distances = parse_input(input_lines)
    print("Part 1: The product of record options is ", prod(record_options(times, distances)))

    times, distances = parse_input_kerning(input_lines)
    print("Part 2: Record options are ", record_options(times, distances)[0])