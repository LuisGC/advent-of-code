from typing import List

class Direction():
    def __init__(self, facing: int):
        self.facing = facing

    def turn_right(self):
        self.facing = (self.facing + 1) % 4

    def turn_left(self):
        self.turn_right()
        self.turn_right()
        self.turn_right()
    
    def delta_row(self) -> int:
        if self.facing == 0: return 0
        elif self.facing == 1: return 1
        elif self.facing == 2: return 0
        else: return -1
    
    def delta_col(self) -> int:
        if self.facing == 0: return 1
        elif self.facing == 1: return 0
        elif self.facing == 2: return -1
        else: return 0


class Maze():
    def __init__(self, lines: List) -> None:
        max_cols = max(map(len, lines))
        self.lines = list(map(lambda l: l.ljust(max_cols), lines))

    def __str__(self) -> str:
        repr = '' + '*' * (2 + len(self.lines[0])) + '\n'
        for row in self.lines:
            repr += '*' + row + '*\n'
        repr += '' + '*' * (2 + len(self.lines[-1])) + '\n'
        return repr

    def starting_position(self):
        for row, line in enumerate(self.lines):
            col = line.find('.')
            if col >= 0:
                return row, col
        raise Exception("Invalid maze")

    def get_tile(self, position: tuple) -> str:
        return self.lines[position[0]][position[1]]

def parse_input(input: str) -> tuple:
    maze, raw_movements = input.split("\n\n")

    movements = raw_movements.replace('R', ' R ').replace('L', ' L ')
    return Maze(maze.splitlines()), movements.strip().split(' ')

def move_step(maze: Maze, position: tuple, direction: Direction) -> tuple:
    row, col = position
    tile = ' '
    while tile == ' ':
        row = (row + direction.delta_row()) % len(maze.lines)
        col = (col + direction.delta_col()) % len(maze.lines[row])
        tile = maze.get_tile((row, col))
    if tile == '.':
        return (row, col), False
    elif tile == '#':
        return position, True

def execute_movements(maze: Maze, movements: List) -> int:
    # print(maze)
    position = maze.starting_position()
    direction = Direction(0)

    for step in movements:
        if step == 'R': direction.turn_right()
        elif step == 'L': direction.turn_left()
        else:
            for _ in range(int(step)):
                position, wall = move_step(maze, position, direction)
                if wall is True: break
    

    return 1000 * (position[0] + 1) + 4*(position[1] + 1) + direction.facing



with open("2022/day-22/example.txt", encoding="utf-8") as f:
    maze, movements = parse_input(f.read())

    assert 6032 == execute_movements(maze, movements)

with open("2022/day-22/input.txt", encoding="utf-8") as f:
    maze, movements = parse_input(f.read())
    
    print("Part 1: The final password is:", execute_movements(maze, movements))
