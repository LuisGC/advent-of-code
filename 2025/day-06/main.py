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

def calculate_r2l(lines: list[str]) -> int:
    rows, cols = len(lines), len(lines[0]) - 1

    total = 0
    numbers = []

    for c in range(cols - 1, -1, -1):
        current = 0

        for r in range(rows):
            x = lines[r][c]

            if x.isnumeric():
                current *= 10
                current += int(x)

            if r == rows - 1 and current != 0:
                numbers.append(current)
                current = 0

            if x in "+*":
                acc = 1 if x == "*" else 0

                for n in numbers:
                    if x == "*":
                        acc *= n
                    else:
                        acc += n
                
                total += acc
                numbers = []

    return total

with open("2025/day-06/example.txt", encoding="utf-8") as f:
    input_lines = [line for line in f.readlines()]

    assert 4277556 == calculate_all(input_lines)
    assert 3263827 == calculate_r2l(input_lines)

with open("2025/day-06/input.txt", encoding="utf-8") as f:
    input_lines = [line for line in f.readlines()]

    print(f"Part 1: The grand total is {calculate_all(input_lines)}")
    print(f"Part 2: The grand total in Cephalopod Math is {calculate_r2l(input_lines)}")
