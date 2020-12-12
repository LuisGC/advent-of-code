CLOCKWISE = "NESWN"
ANTICLOCKWISE = "NWSEN"

def rotate_ship(action, facing, degrees):
    if degrees == 0:
        return facing
    elif degrees == 90:
        if action == 'L':
            return ANTICLOCKWISE[ANTICLOCKWISE.find(facing)+1]
        else:
            return CLOCKWISE[CLOCKWISE.find(facing)+1]
    else:
        return rotate_ship(action, facing, degrees-90)

def move_ship(current_x: int, current_y: int, direction: str, value: int):

    if direction == 'N':
        current_y += value
    elif direction == 'S':
        current_y -= value
    elif direction == 'E':
        current_x += value
    elif direction == 'W':
        current_x -= value

    return current_x, current_y

def navigate (instructions : str):
    x = 0
    y = 0
    facing = 'E'

    for instruction in instructions:
        action = instruction[0]
        value = int(instruction[1:])

        if action in ['N', 'S', 'E', 'W']:
            x, y = move_ship(x, y, action, value)
        elif action == 'F':
            x, y = move_ship(x, y, facing, value)
        elif action == 'L' or action == 'R':
            facing = rotate_ship(action, facing, value)

    print ("Final coords", x,y)
    return x,y

with open("day-12/example.txt") as f:
    instructions = f.readlines()
    x, y = navigate(instructions)
    assert 25 == abs(x) + abs(y)

with open("day-12/input.txt") as f:
    instructions = f.readlines()
    x, y = navigate(instructions)
    print("Part 1: The final Manhattan distance is", abs(x) + abs(y))
