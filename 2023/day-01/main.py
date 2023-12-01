def first_and_last_digits(line: str) -> int:
    first_digit = last_digit = None
    for i in range(len(line)):
        if first_digit is None and line[i].isdigit():
            first_digit = line[i]
        if last_digit is None and line[-i-1].isdigit():
            last_digit = line[-i-1]
        if first_digit is not None and last_digit is not None:
            break
    return int(first_digit + last_digit)

with open("2023/day-01/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = 0
    for line in input_lines:
        total += first_and_last_digits(line)
        print(total)

    assert 142 == total

with open("2023/day-01/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = 0
    for line in input_lines:
        total += first_and_last_digits(line)
        print(total)
        
    print("Part 1:", total)
