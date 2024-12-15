from typing import List, Tuple

ROBOT = "@"
BOX = "O"
WALL = "#"
EMPTY = "."

N, E, S, W = "^>v<"

def get_robot_pos(map: List[List[str]]) -> Tuple[int, int]:
    for y in range(len(map)):
        if ROBOT in map[y]:
            return (map[y].index(ROBOT), y)

def parse_input(input_lines: List) -> Tuple[List[List[str]], Tuple[int, int], str]:
    i_sep = input_lines.index('')
    map = [list(s) for s in input_lines[:i_sep]]
    movements = ''.join(input_lines[i_sep + 1:])

    return (map, get_robot_pos(map), movements)

def next_pos(pos: Tuple[int, int], dir: str) -> Tuple[int, int]:
    x, y = pos
    if dir == N:
        return (x, y - 1)
    elif dir == E:
        return (x + 1, y)
    elif dir == S:
        return (x, y + 1)
    elif dir == W:
        return (x - 1, y)

def move_robot(map: List[List[str]], robot_pos: Tuple[int, int], move: str) -> Tuple[List[List[str]], Tuple[int, int]]:
    sx, sy = robot_pos
    next_x, next_y = next_pos(robot_pos, move)
    x, y = next_x, next_y

    if map[next_y][next_x] == EMPTY:
        map[next_y][next_x] = ROBOT
        map[sy][sx] = EMPTY
        robot_pos = (next_x, next_y)
    elif map[next_y][next_x] == BOX:
        while map[y][x] == BOX:
            x, y = next_pos((x, y), move)

        if map[y][x] == EMPTY:
            map[next_y][next_x] = ROBOT
            map[sy][sx] = EMPTY
            map[y][x] = BOX
            robot_pos = (next_x, next_y)

    return map, robot_pos


def apply_movements(map: List[List[str]], robot_pos: Tuple[int, int], movements: str) -> List[List[str]]:

    for move in movements:
        map, robot_pos = move_robot(map, robot_pos, move)

    return map

def sum_box_coords(map: List[List[str]]) -> int:
    coords = []
    for row in range(len(map)):
        for col in [i for i in range(len(map[row])) if map[row][i] == BOX]:
            coords.append(100 * row + col)
    return sum(coords)


with open("2024/day-15/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    map, pos, movements = parse_input(input_lines)
    map = apply_movements(map, pos, movements)

    assert 2028 == sum_box_coords(map)


with open("2024/day-15/larger-example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    map, pos, movements = parse_input(input_lines)
    map = apply_movements(map, pos, movements)
    assert 10092 == sum_box_coords(map)

with open("2024/day-15/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    map, pos, movements = parse_input(input_lines)
    map = apply_movements(map, pos, movements)

    print(f"Part 1: Sum of all box coords is {sum_box_coords(map)}")
