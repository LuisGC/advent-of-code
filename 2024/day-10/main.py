import sys
sys.path.insert(0, './')
from utils import Matrix, Coord, vector_direction_values

def calculate_score(matrix: Matrix) -> int:

    def calculate_path(x: int, y: int, peaks: list):
        value = int(matrix.get(x, y))
        if value == 9:
            if len([p for p in peaks if p.equals(Coord(x, y))]) == 0:
                peaks.append(Coord(x, y))
        else:
            paths = []
            for dir in vector_direction_values:
                check_dir = Coord(x + dir.x, y + dir.y)
                if matrix.is_in_bounds(check_dir.x, check_dir.y) and int(matrix.get(check_dir.x, check_dir.y)) == value + 1:
                    paths.append(check_dir)
            for p in paths:
                calculate_path(p.x, p.y, peaks)
    
    score = 0
    for y in range(0, matrix.get_row_count()):
        for x in range(0, matrix.get_col_count(y)):
            if int(matrix.get(x, y)) == 0:
                peaks = []
                calculate_path(x, y, peaks)
                score += len(peaks)

    return score

with open("2024/day-10/example.txt", encoding="utf-8") as f:
    matrix = Matrix([line.strip() for line in f.readlines()])
    assert 1 == calculate_score(matrix)

with open("2024/day-10/larger-example.txt", encoding="utf-8") as f:
    matrix = Matrix([line.strip() for line in f.readlines()])
    assert 36 == calculate_score(matrix)

with open("2024/day-10/input.txt", encoding="utf-8") as f:
    matrix = Matrix([line.strip() for line in f.readlines()])

    print(f"Part 1: Sum of all trailheads scores is {calculate_score(matrix)}")
#    print(f"Part 2: Sum of middle page numbers with fix is {sum_middle_pages(input_lines, with_fix=True)}")
