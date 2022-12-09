from typing import List

def parse_input(lines: List) -> List:
    movements = []
    for line in lines:
        direction, quantity = line.split()
        movements.append((direction, int(quantity)))

    return movements

def move_head(direction: str, head: tuple):
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

def move_tail(head: tuple, tail:tuple):
    if abs(head[0]-tail[0]) > 1 or abs(head[1]-tail[1]) > 1:
        tail[0] += close_gap(head[0] - tail[0])
        tail[1] += close_gap(head[1] - tail[1])

def count_tail_visited_positions(head_movements: List) -> int:
    head = [0, 0]
    tail = [0, 0]
    visited = {tuple(tail)}

    for direction, quantity in head_movements:
        for _ in range(quantity):
            move_head(direction, head)
            move_tail(head, tail)
            # print("Head: " + str(head) + " Tail: " + str(tail))
            visited.add(tuple(tail))

    # print(visited)
    return len(visited)


with open("2022/day-09/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    head_movements = parse_input(input_lines)

    assert 13 == count_tail_visited_positions(head_movements)

with open("2022/day-09/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    head_movements = parse_input(input_lines)

    print("Part 1: Count of visited positions by tail are:", count_tail_visited_positions(head_movements))
