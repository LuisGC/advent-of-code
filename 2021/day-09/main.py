from typing import List


def parse_input(input: List[str]) -> (List[int], int, int):

    numbers = []
    size = len(input[0])

    for row in input:
        for pos in range(size):
            numbers.append(int(row[pos]))

    return numbers, size, len(input)


def calculate_basin_size(numbers: List[int], cols: int, rows: int, pos: int) -> int:

    return 1


def calculate_risk_level(numbers: List[int], cols: int, rows: int) -> int:

    sum = 0
    for pos in range(len(numbers)):

        # Checking the corners
        if pos ==  0:
            if numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos+cols]:
                sum += numbers[pos] + 1
        elif pos ==  cols - 1:
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos+cols]:
                sum += numbers[pos] + 1
        elif pos ==  (rows - 1) * cols:
            if numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos-cols]:
                sum += numbers[pos] + 1
        elif pos ==  (rows * cols) - 1:
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos-cols]:
                sum += numbers[pos] + 1
        # Checking the borders
        elif pos < cols:
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos+cols]:
                sum += numbers[pos] + 1
        elif pos % cols == 0:
            if numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos+cols] and numbers[pos] < numbers[pos-cols]:
                sum += numbers[pos] + 1
        elif pos % cols == (cols - 1):
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos+cols] and numbers[pos] < numbers[pos-cols]:
                sum += numbers[pos] + 1
        elif pos > cols * (rows - 1):
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos-cols]:
                sum += numbers[pos] + 1
        # rest of the board
        else:
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos-cols] and numbers[pos] < numbers[pos+cols]:
                sum += numbers[pos] + 1

    return sum


with open("2021/day-09/example.txt") as f:
    input = [str(line.strip()) for line in f]
    numbers, cols, rows = parse_input(input)

    assert 15 == calculate_risk_level(numbers, cols, rows)


with open("2021/day-09/input.txt") as f:
    input = [str(line.strip()) for line in f]
    numbers, cols, rows = parse_input(input)

    print("Part 1: Sum of the risk level is", calculate_risk_level(numbers, cols, rows))
#     print("Part 2: Bingo loser score is", play_to_lose(draws, cards))
