from typing import List

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

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
        if self.facing == RIGHT: return 0
        elif self.facing == DOWN: return 1
        elif self.facing == LEFT: return 0
        else: return -1 # UP
    
    def delta_col(self) -> int:
        if self.facing == RIGHT: return 1
        elif self.facing == DOWN: return 0
        elif self.facing == LEFT: return -1
        else: return 0 # UP

DIR_UP = Direction(UP)
DIR_DOWN = Direction(DOWN)
DIR_LEFT = Direction(LEFT)
DIR_RIGHT = Direction(RIGHT)

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

    def move_step(self, position: tuple, direction: Direction) -> tuple:
        row, col = position
        tile = ' '
        while tile == ' ':
            row = (row + direction.delta_row()) % len(self.lines)
            col = (col + direction.delta_col()) % len(self.lines[row])
            tile = self.get_tile((row, col))
        if tile == '.':
            return (row, col), direction, False
        elif tile == '#':
            return position, direction, True

class Side:
    def __init__(self, top, left) -> None:
        self.connected = {}
        self.top = top
        self.left = left

    def __repr__(self) -> str:
        return(f"({self.top}, {self.left})")

class CubeMaze(Maze):

    def __init__(self, lines: List) -> None:
        super().__init__(lines)
        side_len = self.get_side_len()
        self.sides = []
        for row in range(0, len(self.lines), side_len):
            for col in range(0, len(self.lines[0]), side_len):
                if self.get_tile((row, col)) != ' ':
                    self.sides.append(Side(row, col))
        assert len(self.sides) == 6

        self.create_initial_connections(side_len)
        self.complete_connections()

    def create_initial_connections(self, side_len: int):
        for index, side1 in enumerate(self.sides):
            for side2 in self.sides[index + 1:]:
                if side1.top == side2.top:
                    if side1.left == side2.left - side_len:
                        side1.connected[RIGHT] = (side2, 0)
                        side2.connected[LEFT] = (side1, 0)
                    elif side1.left == side2.left + side_len:
                        side1.connected[LEFT] = (side2, 0)
                        side2.connected[RIGHT] = (side1, 0)
                if side1.left == side2.left:
                    if side1.top == side2.top - side_len:
                        side1.connected[DOWN] = (side2, 0)
                        side2.connected[UP] = (side1, 0)
                    elif side1.top == side2.top + side_len:
                        side1.connected[UP] = (side2, 0)
                        side2.connected[DOWN] = (side1, 0)
    
    def complete_connections(self):
        added = False
        for side in self.sides:
            for direction in range(4):
                if side.connected.get(direction) is None:
                    added = added or self.check_and_add(side, direction)
        if added:
            self.complete_connections()

    def check_and_add(self, side: Side, direction: int):
        for deroute in [-1, 1]:
            deroute_direction = (direction + deroute) % 4
            if side.connected.get(deroute_direction):
                middle, middle_turn = side.connected.get(deroute_direction)
                check_direction = (direction + middle_turn + 4) % 4
                if middle.connected.get(check_direction):
                    target, target_turn = middle.connected.get(check_direction)
                    side.connected[direction] = (target, (middle_turn + target_turn + deroute + 4) % 4)
                    return True
        return False

    def get_side_len(self) -> int:
        if len(self.lines) == len(self.lines[0]):
            return len(self.lines) // 3
        else:
            return max(len(self.lines), len(self.lines[0])) // 4

    def get_local_position_on_side(self, position) -> tuple:
        side_len = self.get_side_len()
        return (position[0] + side_len) % side_len, (position[1] + side_len) % side_len

    def move_step(self, position: tuple, direction: Direction) -> tuple:
        current_side_index = self.get_side_index(position)
        new_position = self.new_position_after_step(position, direction)
        new_side_index = self.get_side_index(new_position)
        new_direction = direction
        if current_side_index != new_side_index:
            local_row, local_col = self.get_local_position_on_side(new_position)
            mlen = self.get_side_len() - 1
            new_side, turn = self.sides[current_side_index].connected[direction.facing]
            new_direction = Direction((direction.facing + turn + 4) % 4)
            transitions = [
                [(local_row, 0), (0, mlen - local_row), (mlen - local_row, mlen), (mlen, local_row)], # Right
                [(0, local_col), (local_col, mlen), (mlen, mlen - local_col), (mlen - local_col, 0)], # Down
                [(local_row, mlen), (mlen, mlen - local_row), (mlen - local_row, 0), (0, local_row)], # Left
                [(mlen, local_col), (local_col, 0), (0, mlen - local_col), (mlen - local_col, mlen)]  # Up
            ]
            new_row, new_col = transitions[direction.facing][turn]
            new_position = (new_side.top + new_row, new_side.left + new_col)
        tile = self.get_tile(new_position)
        if tile == '.':
            return new_position, new_direction, False
        elif tile == '#':
            return position, direction, True

    @staticmethod
    def new_position_after_step(position: tuple, direction: Direction) -> tuple:
        new_row = position[0] + direction.delta_row()
        new_col = position[1] + direction.delta_col()
        return new_row, new_col

    def get_side_index(self, position: tuple) -> int:
        for index, side in enumerate(self.sides):
            if side.left <= position[1] < side.left + self.get_side_len() and side.top <= position[0] < side.top + self.get_side_len():
                return index
        return -9999

def parse_input(input: str, cube: bool = False) -> tuple:
    maze, raw_movements = input.split("\n\n")

    movements = raw_movements.replace('R', ' R ').replace('L', ' L ')
    if cube:
        return CubeMaze(maze.splitlines()), movements.strip().split(' ')
    else:
        return Maze(maze.splitlines()), movements.strip().split(' ')        

def calculate_password(position: tuple, direction: Direction) -> int:
    return 1000 * (position[0] + 1) + 4*(position[1] + 1) + direction.facing

def execute_movements(maze: Maze, movements: List) -> int:
    position = maze.starting_position()
    direction = DIR_RIGHT

    for step in movements:
        if step == 'R': direction.turn_right()
        elif step == 'L': direction.turn_left()
        else:
            for _ in range(int(step)):
                position, direction, wall = maze.move_step(position, direction)
                if wall is True: break
    
    return calculate_password(position, direction)



with open("2022/day-22/example.txt", encoding="utf-8") as f:
    lines = f.read()
    maze, movements = parse_input(lines)
    assert 6032 == execute_movements(maze, movements)
    maze, movements = parse_input(lines, cube=True)
    assert 5031 == execute_movements(maze, movements)

with open("2022/day-22/input.txt", encoding="utf-8") as f:
    lines = f.read()
    maze, movements = parse_input(lines)
    print("Part 1: The final password is:", execute_movements(maze, movements))
    maze, movements = parse_input(lines, cube=True)
    print("Part 2: The final password for the cube is:", execute_movements(maze, movements))
