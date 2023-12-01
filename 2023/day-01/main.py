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

def rewrite_digits(line: str) -> str:
    new_line = line.replace("oneight", "18")
    new_line = new_line.replace("twone", "21")
    new_line = new_line.replace("threeight", "38")
    new_line = new_line.replace("fiveight", "58")
    new_line = new_line.replace("sevenine", "79")
    new_line = new_line.replace("eightwo", "82")
    new_line = new_line.replace("eighthree", "83")
    new_line = new_line.replace("nineighth", "98")

    new_line = new_line.replace("one", "1").replace("two", "2").replace("three", "3")
    new_line = new_line.replace("four", "4").replace("five", "5").replace("six", "6")
    new_line = new_line.replace("seven", "7").replace("eight", "8").replace("nine", "9")

    return new_line

with open("2023/day-01/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = 0
    for line in input_lines:
        total += first_and_last_digits(line)

    assert 142 == total

with open("2023/day-01/example2.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = 0
    for line in input_lines:
        total += first_and_last_digits(rewrite_digits(line))

    assert 281 == total


with open("2023/day-01/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = 0
    total2 = 0
    for line in input_lines:
        total += first_and_last_digits(line)
        total2 += first_and_last_digits(rewrite_digits(line))

    print("Part 1:", total)
    print("Part 2:", total2)
