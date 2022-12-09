from typing import List, Tuple

def parse_input(lines: List) -> List:
    movements = []
    for line in lines:
        direction, quantity = line.split()
        movements.append((direction, int(quantity)))

    return movements

def move_head(direction: str, head: List[int]):
    if direction == "R":
        head[0] += 1
    elif direction == "L":
        head[0] -= 1
    elif direction == "U":
        head[1] += 1
    else:
        head[1] -= 1

def close_gap(gap: int) -> int:
    if gap > 0:
        return 1
    elif gap <0:
        return -1
    else:
        return 0

def move_tail(head: List[int], tail: List[int]):
    if abs(head[0]-tail[0]) > 1 or abs(head[1]-tail[1]) > 1:
        tail[0] += close_gap(head[0] - tail[0])
        tail[1] += close_gap(head[1] - tail[1])

def count_tail_visited_positions(head_movements: List, knots_quantity: int=1) -> int:
    knots: List[List[int]] = [[0, 0] for _ in range(knots_quantity + 1)]
    visited = {tuple(knots[-1])}

    for direction, quantity in head_movements:
        for _ in range(quantity):
            move_head(direction, knots[0])
            for knot_index in range(1, knots_quantity + 1):
                move_tail(knots[knot_index - 1], knots[knot_index])
            # print("Head: " + str(head) + " Tail: " + str(tail))
            visited.add(tuple(knots[-1]))

    # print(visited)
    return len(visited)


with open("2022/day-09/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    head_movements = parse_input(input_lines)

    assert 13 == count_tail_visited_positions(head_movements)
    assert 1 == count_tail_visited_positions(head_movements, 9)

with open("2022/day-09/larger_example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    head_movements = parse_input(input_lines)

    assert 36 == count_tail_visited_positions(head_movements, 9)

with open("2022/day-09/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    head_movements = parse_input(input_lines)

    print("Part 1: Count of visited positions by tail are:", count_tail_visited_positions(head_movements))
    print("Part 2: Count of visited positions by 9th knot are:", count_tail_visited_positions(head_movements, 9))
