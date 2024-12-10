import re

mul_pattern = r"mul\((\d+),(\d+)\)"

def adding_muls(lines: list) -> int:

    matches = re.findall(mul_pattern, lines)

    total = sum(int(x) * int (y) for x, y in matches)

    return total

with open("2024/day-03/example.txt", encoding="utf-8") as f:
    input_lines = f.read()
    assert 161 == adding_muls(input_lines)

with open("2024/day-03/input.txt", encoding="utf-8") as f:
    input_lines = f.read()

    print(f"Part 1: Adding the muls is {adding_muls(input_lines)}")
#    print(f"Part 2: Amount of safe lines with tolerance is {safe_lines(input_lines, tolerate_bad = True)}")
