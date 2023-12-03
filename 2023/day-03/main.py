from itertools import product

def is_part(char: str) -> bool:
    return char not in ".0123456789"

def get_part_numbers(lines: list) -> int:
    total = 0

    for i in range(len(lines)):
        initial_digit_pos = None
        near_part = False

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
            else:
                if initial_digit_pos is not None:
                    if near_part:
                        total += int(lines[i][initial_digit_pos:j])
                    
                    initial_digit_pos = None
                    near_part = False

    return total


with open("2023/day-03/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 4361 == get_part_numbers(input_lines)

with open("2023/day-03/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print("Part 1: Sum of all part numbers is ", get_part_numbers(input_lines))
