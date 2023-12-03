digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def numify_line(line: str, letters_are_valid: bool = False) -> str:
    new_line = ""
    for index in range(len(line)):
        if letters_are_valid and any(line[index:].startswith(digit := item) for item in digits):
            new_line += str(digits.index(digit) + 1)
        elif str.isdigit(line[index]):
            new_line += line[index]
    return new_line

with open("2023/day-01/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = 0
    for line in input_lines:
        new_line = numify_line(line)
        total += int(new_line[0] + new_line[-1]) if len(new_line) > 0 else 0

    assert 142 == total

with open("2023/day-01/example2.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = 0
    for line in input_lines:
        new_line = numify_line(line, True)
        total += int(new_line[0] + new_line[-1]) if len(new_line) > 0 else 0

    assert 281 == total

with open("2023/day-01/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = 0
    total2 = 0
    for line in input_lines:
        new_line = numify_line(line)
        total += int(new_line[0] + new_line[-1]) if len(new_line) > 0 else 0

        new_line = numify_line(line, True)
        total2 += int(new_line[0] + new_line[-1]) if len(new_line) > 0 else 0

    print(f"Part 1: Sum of all calibrations is {total}")
    print(f"Part 2: Sum of all calibrations (nums in letters are valid) is {total2}")
