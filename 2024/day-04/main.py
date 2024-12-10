def count_XMAS(lines: list) -> int:

    rows = len(lines)
    cols = len(lines[0])

    xmas_count = 0
    for r in range(rows):
        for c in range(cols):
            if c+3<cols and lines[r][c]=='X' and lines[r][c+1]=='M' and lines[r][c+2]=='A' and lines[r][c+3]=='S':
                xmas_count += 1
            if c+3<cols and lines[r][c]=='S' and lines[r][c+1]=='A' and lines[r][c+2]=='M' and lines[r][c+3]=='X':
                xmas_count += 1
            if r+3<rows and lines[r][c]=='X' and lines[r+1][c]=='M' and lines[r+2][c]=='A' and lines[r+3][c]=='S':
                xmas_count += 1
            if r+3<rows and lines[r][c]=='S' and lines[r+1][c]=='A' and lines[r+2][c]=='M' and lines[r+3][c]=='X':
                xmas_count += 1
            if r+3<rows and c+3<cols and lines[r][c]=='X' and lines[r+1][c+1]=='M' and lines[r+2][c+2]=='A' and lines[r+3][c+3]=='S':
                xmas_count += 1
            if r+3<rows and c+3<cols and lines[r][c]=='S' and lines[r+1][c+1]=='A' and lines[r+2][c+2]=='M' and lines[r+3][c+3]=='X':
                xmas_count += 1
            if r-3>=0 and c+3<cols and lines[r][c]=='X' and lines[r-1][c+1]=='M' and lines[r-2][c+2]=='A' and lines[r-3][c+3]=='S':
                xmas_count += 1
            if r-3>=0 and c+3<cols and lines[r][c]=='S' and lines[r-1][c+1]=='A' and lines[r-2][c+2]=='M' and lines[r-3][c+3]=='X':
                xmas_count += 1

    return xmas_count

def count_X_MAS(lines: list) -> int:

    rows = len(lines)
    cols = len(lines[0])

    xmas_count = 0
    for r in range(rows):
        for c in range(cols):
            if r+2<rows and c+2<cols:
                if lines[r][c]=='M' and lines[r+1][c+1]=='A' and lines[r+2][c+2]=='S' and lines[r+2][c]=='M' and lines[r][c+2]=='S':
                    xmas_count += 1
                if lines[r][c]=='M' and lines[r+1][c+1]=='A' and lines[r+2][c+2]=='S' and lines[r+2][c]=='S' and lines[r][c+2]=='M':
                    xmas_count += 1
                if lines[r][c]=='S' and lines[r+1][c+1]=='A' and lines[r+2][c+2]=='M' and lines[r+2][c]=='M' and lines[r][c+2]=='S':
                    xmas_count += 1
                if lines[r][c]=='S' and lines[r+1][c+1]=='A' and lines[r+2][c+2]=='M' and lines[r+2][c]=='S' and lines[r][c+2]=='M':
                    xmas_count += 1

    return xmas_count

with open("2024/day-04/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 18 == count_XMAS(input_lines)
    assert 9 == count_X_MAS(input_lines)

with open("2024/day-04/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: XMAS found times is {count_XMAS(input_lines)}")
    print(f"Part 2: X-MAS found times is {count_X_MAS(input_lines)}")
