from typing import List, Tuple
import sys
sys.path.insert(0, './')
from utils import profiler

def parse_input(input: str) -> List:
    lines = []
    for line in input.split("\n"):
        res, val = line.split(":")
        result = int(res)
        values = [int(x) for x in val.split()]
        lines.append((result, values))
    return lines

def fix_equation(line: Tuple, operators: int) -> int:
    result, values = line
    for x in range(operators):
        left = values[0]
        right = values[1]
        match x:
            case 0:
                left = left * right
            case 1:
                left = left + right
            case 2:
                left = int(str(left) + str(right))
        if left > result:
            continue
        next_values = [left] + values[2:]
        if len(next_values) < 2:
            if left == result:
                return result
        elif fix_equation((result, next_values), operators) == result:
            return result
    return 0

@profiler
def total_calibration(lines: List, operators: int = 2) -> int:
    result = 0
    for line in lines:
        result += fix_equation(line, operators)
    return result

with open("2024/day-07/example.txt", encoding="utf-8") as f:
    lines = parse_input(f.read().rstrip())
    assert 3749 == total_calibration(lines)
    assert 11387 == total_calibration(lines, operators = 3)

with open("2024/day-07/input.txt", encoding="utf-8") as f:
    lines = parse_input(f.read().rstrip())
    print(f"Part 1: Total calibration result is {total_calibration(lines)}")
    print(f"Part 2: Total calibration result with 3 operators is {total_calibration(lines, operators = 3)}")
