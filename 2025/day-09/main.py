import sys
sys.path.insert(0, './')
from utils import profiler

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

@profiler
def largest_rectangle_area(grid: list[tuple[int, int]]) -> int:
    return max(calculate_area(grid[i], grid[j]) for i in range(len(grid)) for j in range(i + 1, len(grid)))

def get_segments(red_tiles: list[tuple[int, int]]) -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    v_segments = []
    h_segments = []

    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]

        if x1 == x2:  # vertical segment
            v_segments.append((x1, min(y1, y2), max(y1, y2)))
        elif y1 == y2:  # horizontal segment
            h_segments.append((y1, min(x1, x2), max(x1, x2)))

    return v_segments, h_segments

def point_on_boudary(x: int, y: int, v_segments: list[tuple[int, int, int]], h_segments: list[tuple[int, int, int]]) -> bool:
    for vx, vy_start, vy_end in v_segments:
        if x == vx and vy_start <= y <= vy_end:
            return True
    for hy, hx_start, hx_end in h_segments:
        if y == hy and hx_start <= x <= hx_end:
            return True
    return False

def point_inside_polygon(x: int, y: int, v_segments: list[tuple[int, int, int]], h_segments: list[tuple[int, int, int]]) -> bool:
    crossings = 0
    for vx, vy_start, vy_end in v_segments:
        if vx > x and vy_start <= y <= vy_end:
            crossings += 1
    return crossings % 2 == 1

def valid_point(x: int, y: int, v_segments: list[tuple[int, int, int]], h_segments: list[tuple[int, int, int]]) -> bool:
    return point_on_boudary(x, y, v_segments, h_segments) or point_inside_polygon(x, y, v_segments, h_segments)

def valid_rectangle(x_min: int, x_max: int, y_min: int, y_max: int, v_segments: list[tuple[int, int, int]], h_segments: list[tuple[int, int, int]]) -> bool:
    # check the four corners
    corners = [(x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max)]
    for cx, cy in corners:
        if not valid_point(cx, cy, v_segments, h_segments):
            return False
        
    # check if any vertical polygon edge crosses through the rectangle
    for x, y_start, y_end in v_segments:
        if x_min < x < x_max and (y_start < y_max and y_end > y_min):
            return False
        
    # check if any horizontal polygon edge crosses through the rectangle
    for y, x_start, x_end in h_segments:
        if y_min < y < y_max and (x_start < x_max and x_end > x_min):
            return False        
    return True

@profiler
def largest_rectangle_area_with_green(red_tiles: list[tuple[int, int]]) -> int:
    max_area = 0

    v_segments, h_segments = get_segments(red_tiles)

    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            corner1 = red_tiles[i]
            corner2 = red_tiles[j]
            x_min, x_max = min(corner1[0], corner2[0]), max(corner1[0], corner2[0])
            y_min, y_max = min(corner1[1], corner2[1]), max(corner1[1], corner2[1])

            if valid_rectangle(x_min, x_max, y_min, y_max, v_segments, h_segments):
                width = x_max - x_min + 1
                height = y_max - y_min + 1
                max_area = max(max_area, width * height)
    return max_area

with open("2025/day-09/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    grid = parse_input(input_lines)

    assert 50 == largest_rectangle_area(grid)
    assert 24 == largest_rectangle_area_with_green(grid)

with open("2025/day-09/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    grid = parse_input(input_lines)

    print(f"Part 1: The largest rectangle area is {largest_rectangle_area(grid)}")
    print(f"Part 2: The largest rectangle area with red and green tiles is {largest_rectangle_area_with_green(grid)}")
