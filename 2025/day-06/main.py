def calculate_all(lines: list[str]) -> int:
    total = 0
    numbers = []

    for r, row in enumerate(lines):
        cols = row.split()

        if r == len(lines) - 1:
            for c, op in enumerate(cols):
                acc = 1 if op == "*" else 0

                for i in range(len(numbers)):
                    if op == "*":
                        acc *= numbers[i][c]
                    else:
                        acc += numbers[i][c]
                total += acc
        else:
            numbers.append([int(x) for x in cols])

    return total

with open("2025/day-06/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    assert 4277556 == calculate_all(input_lines)

with open("2025/day-06/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: The grand total is {calculate_all(input_lines)}")
#    print(f"Part 2: The grand total is {count_all_fresh(ranges)}")
