from typing import List


def parse_input(input: List[str]) -> (List[int], int, int):

    numbers = []
    size = len(input[0])

    for row in input:
        for pos in range(size):
            numbers.append(int(row[pos]))

    return numbers, size, len(input)


def obtain_low_points(numbers: List[int], cols: int, rows: int) -> List[int]:

    low_points = []
    for pos in range(len(numbers)):

        # Checking the corners
        if pos ==  0:
            if numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos+cols]:
                low_points.append(pos)
        elif pos ==  cols - 1:
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos+cols]:
                low_points.append(pos)
        elif pos ==  (rows - 1) * cols:
            if numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos-cols]:
                low_points.append(pos)
        elif pos ==  (rows * cols) - 1:
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos-cols]:
                low_points.append(pos)
        # Checking the borders
        elif pos < cols:
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos+cols]:
                low_points.append(pos)
        elif pos % cols == 0:
            if numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos+cols] and numbers[pos] < numbers[pos-cols]:
                low_points.append(pos)
        elif pos % cols == (cols - 1):
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos+cols] and numbers[pos] < numbers[pos-cols]:
                low_points.append(pos)
        elif pos > cols * (rows - 1):
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos-cols]:
                low_points.append(pos)
        # rest of the board
        else:
            if numbers[pos] < numbers[pos-1] and numbers[pos] < numbers[pos+1] and numbers[pos] < numbers[pos-cols] and numbers[pos] < numbers[pos+cols]:
                low_points.append(pos)

    return low_points


def calculate_risk_level(numbers: List[int], low_points: List[int]) -> int:
    sum = 0
    for pos in low_points:
        sum += numbers[pos] + 1
    return sum


def create_basin(numbers: List[int], cols:int, rows:int, pos: int) -> List[int]:

    basin_area = []
    next_coords = []
    if numbers[pos] == 9:
        return []
    elif pos not in basin_area:
        basin_area.append(pos)

    if pos // cols > 0 and numbers[pos] < numbers[pos-cols]:
        next_coords += create_basin(numbers, cols, rows, pos-cols)

    if pos // cols < rows - 1 and numbers[pos] < numbers[pos+cols]:
        next_coords += create_basin(numbers, cols, rows, pos+cols)

    if pos % cols > 0 and numbers[pos] < numbers[pos-1]:
        next_coords += create_basin(numbers, cols, rows, pos-1)

    if pos % cols < cols - 1 and numbers[pos] < numbers[pos+1]:
        next_coords += create_basin(numbers, cols, rows, pos+1)


    if len(next_coords) > 0:
        basin_area += next_coords

    return basin_area


def calculate_basin_sizes(numbers: List[int], cols : int, rows: int, low_points: List[int]) -> List[int]:
    sizes = []
    for pos in low_points:
        basin = set(create_basin(numbers, cols, rows, pos))
        sizes.append(len(basin))

    return sizes


with open("2021/day-09/example.txt", encoding="utf-8") as f:
    input = [str(line.strip()) for line in f]
    numbers, cols, rows = parse_input(input)
    low_points = obtain_low_points(numbers, cols, rows)

    assert 15 == calculate_risk_level(numbers, low_points)

    basin_sizes = sorted(calculate_basin_sizes(numbers, cols, rows, low_points))
    assert 1134 == basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]


with open("2021/day-09/input.txt", encoding="utf-8") as f:
    input = [str(line.strip()) for line in f]
    numbers, cols, rows = parse_input(input)
    low_points = obtain_low_points(numbers, cols, rows)

    print("Part 1: Sum of the risk level is", calculate_risk_level(numbers, low_points))

    basin_sizes = sorted(calculate_basin_sizes(numbers, cols, rows, low_points))
    print("Part 2: Risk level in the three larges basins is", basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])
