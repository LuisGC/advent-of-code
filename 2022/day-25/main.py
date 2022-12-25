from typing import List

base_5 = {
    "2" : 2,
    "1" : 1,
    "0" : 0,
    "-" : -1,
    "=" : -2
}

def parse_snafu(snafu: str) -> int:
    total = 0
    for index, char in enumerate(reversed(snafu)):
        digit_value = base_5[char] * pow(5, index)
        total += digit_value
    return total

def snafu(number: int) -> str:
    snafu = ""
    partial = number
    while partial:
        digit = partial % 5
        if digit == 0:
            snafu = "0" + snafu
        elif digit == 1:
            snafu = "1" + snafu
        elif digit == 2:
            snafu = "2" + snafu
        elif digit == 3:
            snafu = "=" + snafu
            partial += 2
        elif digit == 4:
            snafu = "-" + snafu
            partial += 1
        
        partial = partial // 5

    return snafu

def get_snafu_input(lines: List) -> str:
    code = sum([parse_snafu(line) for line in lines])
    return snafu(code)

with open("2022/day-25/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert "2=-1=0" == get_snafu_input(input_lines)

with open("2022/day-25/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    print("Part 1: SNAFU code is:", get_snafu_input(input_lines))
