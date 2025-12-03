def largest_joltage(input: list[list[int]]) -> int:
    largest = 0
    for line in input:
        best: list[int] = []
        remaining = line
        for i in range(2):
            best_digit = max(remaining[:len(remaining) + i + 1 - 2])
            best_index = remaining.index(best_digit)
            best.append(best_digit)
            remaining = remaining[best_index + 1 :]

        largest += int("".join(str(digit) for digit in best))

    return largest

with open("2025/day-03/example.txt", encoding="utf-8") as f:
    input_lines = [[int(char) for char in line.strip()] for line in f.readlines()]
    assert 357 == largest_joltage(input_lines)

with open("2025/day-03/input.txt", encoding="utf-8") as f:
    input_lines = [[int(char) for char in line.strip()] for line in f.readlines()]

    print(f"Part 1: The largest joltage is {largest_joltage(input_lines)}")
#    print(f"Part 2: The largest joltage is {largest_joltage(input_lines)}")
