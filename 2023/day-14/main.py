from typing import List, Tuple

def parse_input (platform: List[str]) -> List[Tuple[int, int]]:
    return [(i, j) for i in range(len(platform)) for j in range(len(platform[0])) if platform[i][j] == 'O']

def tilt_and_weight(platform: List[str], rocks: List[Tuple[int, int]]) -> int:
    weight = 0
    for rock in rocks:
        row, col = rock[0], rock[1]
        weight += len(platform) - row
        if row > 0:
            for i, upper_row in enumerate(platform[:row][::-1], 1):
                if upper_row[col] == '.':
                    weight += 1
                    platform[row - i][col]  = 'O'
                    platform[row - i + 1][col]  = '.'
                else:
                    break

    return weight


with open("2023/day-14/example.txt", encoding="utf-8") as f:
    platform = [list(line.strip()) for line in f.readlines()]
    rocks = parse_input(platform)

    assert 136 == tilt_and_weight(platform, rocks)

with open("2023/day-14/input.txt", encoding="utf-8") as f:
    platform = [list(line.strip()) for line in f.readlines()]
    rocks = parse_input(platform)
    
    print("Part 1: The sum of all mirrors is ", tilt_and_weight(platform, rocks))
