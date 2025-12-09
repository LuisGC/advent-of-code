def parse_input(input_lines):
    grid = []
    for line in input_lines:
        x, y = map(int, line.split(","))
        grid.append((x, y))
    return grid

def calculate_area(corner1: tuple[int, int], corner2: tuple[int, int]) -> int:
    x1, x2 = min(corner1[0], corner2[0]), max(corner1[0], corner2[0])
    y1, y2 = min(corner1[1], corner2[1]), max(corner1[1], corner2[1])
    return (x2 - x1 + 1) * (y2 - y1 + 1)

def largest_rectangle_area(grid: list[tuple[int, int]]) -> int:
    return max(calculate_area(grid[i], grid[j]) for i in range(len(grid)) for j in range(i + 1, len(grid)))

with open("2025/day-09/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    grid = parse_input(input_lines)

    assert 50 == largest_rectangle_area(grid)

with open("2025/day-09/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    grid = parse_input(input_lines)

    print(f"Part 1: The largest rectangle area is {largest_rectangle_area(grid)}")
