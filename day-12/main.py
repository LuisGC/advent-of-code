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
        if action == 'L':
            return rotate_ship(action, ANTICLOCKWISE[ANTICLOCKWISE.find(facing)+1], degrees-90)
        else:
            return rotate_ship(action, CLOCKWISE[CLOCKWISE.find(facing)+1], degrees-90)


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

    return x,y


def waypoint_navigate (instructions : str):
    waypoint_x = 10
    waypoint_y = 1
    x = 0
    y = 0

    for instruction in instructions:
        action = instruction[0]
        value = int(instruction[1:])

        if action in ['N', 'S', 'E', 'W']:
            waypoint_x, waypoint_y = move_ship(waypoint_x, waypoint_y, action, value)
        elif action == 'L':
            for _ in range(value // 90):
                waypoint_x, waypoint_y = -waypoint_y, waypoint_x
        elif action == 'R':
            for _ in range(value // 90):
                waypoint_x, waypoint_y = waypoint_y, -waypoint_x
        elif action == 'F':
            x += value * waypoint_x
            y += value * waypoint_y

    return x, y


def manhattan_distance (x: int, y: int) -> int:
    return abs(x) + abs(y)


with open("day-12/example.txt") as f:
    instructions = f.readlines()
    x, y = navigate(instructions)
    assert 25 == manhattan_distance(x, y)
    x, y = waypoint_navigate(instructions)
    assert 286 == manhattan_distance(x, y)

with open("day-12/input.txt") as f:
    instructions = f.readlines()
    x, y = navigate(instructions)
    print("Part 1: The final Manhattan distance is", manhattan_distance(x, y))
    x, y = waypoint_navigate(instructions)
    print("Part 2: The final Manhattan distance using waypoints is", manhattan_distance(x, y))
