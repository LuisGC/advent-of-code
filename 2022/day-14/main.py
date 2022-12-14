from typing import List

def solve_cave(cave: List) -> int:
    while True:
        sand_x = 500
        sand_y = 0
        while sand_y + 1 < len(cave):
            for x in (0, -1, 1):
                if cave[1 + sand_y][x + sand_x] == '.':
                    sand_x += x
                    sand_y += 1
                    break
            else:
                cave[sand_y][sand_x] = 'o'
                break
        if sand_y + 1 >= len(cave) or cave[0][500] == 'o':
            return sum (1 for row in cave for c in row if c == 'o')


def obtain_cave(rocks: List, with_floor: bool = False) -> List:
    width = max(max(x for x, y in rock) for rock in rocks) + 200
    height = max(max(y for x, y in rock) for rock in rocks) + 1
    if with_floor:
        cave = [['.' for _ in range(width)] for _ in range(2 + height)]
        for x in range(width):
            cave[height+1][x] = '#'
    else:
        cave = [['.' for _ in range(width)] for _ in range(height)]

    for rock in rocks:
        for (x1, y1), (x2, y2) in zip(rock, rock[1:]):
            for x in range(min(x1, x2), 1 + max(x1, x2)):
                for y in range(min(y1, y2), 1 + max(y1, y2)):
                    cave[y][x] = '#'

    return cave

with open("2022/day-14/example.txt", encoding="utf-8") as f:
    rocks = [[list(map(int, pos.split(','))) for pos in line.strip().split(" -> ")] for line in f.readlines()]
    cave = obtain_cave(rocks)
    assert 24 == solve_cave(cave)
    cave = obtain_cave(rocks, True)
    assert 93 == solve_cave(cave)

with open("2022/day-14/input.txt", encoding="utf-8") as f:
    rocks = [[list(map(int, pos.split(','))) for pos in line.strip().split(" -> ")] for line in f.readlines()]
    cave = obtain_cave(rocks)
    print("Part 1: Filled cave has:", solve_cave(cave))
    cave = obtain_cave(rocks, True)
    print("Part 2: Filled cave with floor has:", solve_cave(cave))
