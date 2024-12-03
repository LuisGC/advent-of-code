from typing import Tuple, List

def is_valid_line(line: str) -> bool:
    descending = False
    if line[0] - line[1] > 0:
        descending = True
    
    is_valid = True
    for i in range(1, len(line)):
        if descending:
            if not (line[i-1] - line[i] > 0 and line[i-1] - line[i] <= 3):
                is_valid = False
                break
        else: # ascending
            if not (line[i] - line[i-1] > 0 and line[i] - line[i-1] <= 3):
                is_valid = False
                break

    return is_valid

def safe_lines(list: List, tolerate_bad: bool = False) -> int:

    safe_count = 0
    for line in list:
        nums = [int(x) for x in line.split(" ")]
        if is_valid_line(nums):
            safe_count += 1
        elif tolerate_bad:
            for i in range(len(nums)):
                fixed = nums.copy()
                del fixed[i]
                if is_valid_line(fixed):
                    safe_count += 1
                    break
            
    return safe_count

with open("2024/day-02/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 2 == safe_lines(input_lines)
    assert 4 == safe_lines(input_lines, tolerate_bad = True)

with open("2024/day-02/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: Amount of safe lines is {safe_lines(input_lines)}")
    print(f"Part 2: Amount of safe lines with tolerance is {safe_lines(input_lines, tolerate_bad = True)}")
