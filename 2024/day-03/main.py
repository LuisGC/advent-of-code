import re

def adding_muls(lines: str, with_flags: bool= False) -> int:

    total = 0
    if with_flags:
        enabled = True
        matches = re.findall(r"(mul\((\d+),(\d+)\)|do\(\)|don\'t(\))", lines)
        for m in matches:
            if m[0] == 'don\'t()':
                enabled = False
            elif m[0] == 'do()':
                enabled = True
            if enabled and 'mul' in m[0]:
                total += int(m[1]) * int(m[2])
    else:
        matches = re.findall(r"mul\((\d+),(\d+)\)", lines)

        total = sum(int(x) * int (y) for x, y in matches)

    return total

with open("2024/day-03/example.txt", encoding="utf-8") as f:
    input_lines = f.read()
    assert 161 == adding_muls(input_lines)
    assert 48 == adding_muls(input_lines, with_flags=True)

with open("2024/day-03/input.txt", encoding="utf-8") as f:
    input_lines = f.read()

    print(f"Part 1: Adding the muls is {adding_muls(input_lines)}")
    print(f"Part 2: Adding the muls with dos and donts is {adding_muls(input_lines, with_flags = True)}")
