from typing import List

def parse_input (lines: List[str]) -> List[str]:
    return lines[0].strip().split(",")

def step_hash(step: str) -> int:
    value = 0
    for char in step:
        value += ord(char)
        value *= 17
        value %= 256

    return value

def total_hash(steps: List[str]) -> int:
    total = 0
    for step in steps:
        step_value = step_hash(step)
        total += step_value
    return total

with open("2023/day-15/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    steps = parse_input(input_lines)
    assert 1320 == total_hash(steps)

with open("2023/day-15/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    steps = parse_input(input_lines)
    print("Part 1: Sum of distance of all galaxies is ", total_hash(steps))