from typing import List

def parse_input (lines: List[str]) -> List[str]:
    return lines[0].strip().split(",")

def label_hash(label: str) -> int:
    value = 0
    for char in label:
        value += ord(char)
        value *= 17
        value %= 256

    return value

def total_hash(steps: List[str]) -> int:
    total = 0
    for step in steps:
        step_value = label_hash(step)
        total += step_value
    return total

def remove_duplicate_lens(box: List[str], label: str):
    for index, value in enumerate(box):
        if label == value[0]:
            box.pop(index)
            break

def set_focal_length(boxes: List[List[int]], label: str, box_number: int, focal_length: int):
    found =  False
    for pos, value in enumerate(boxes[box_number]):
        if label == value[0]:
            boxes[box_number][pos] = (label, focal_length)
            found = True
            break
    
    if not found:
        boxes[box_number].append((label, focal_length))

def calculate_power(boxes: List[List[int]]) -> int:
    power = 0
    for i, box in enumerate(boxes):
        if box:
            for j, lens in enumerate(box):
                lens_power =  (i + 1) * (j + 1) * lens[1]
                power += lens_power

    return power

def focusing_power(steps: List[str]) -> int:
    boxes = [[] for _ in range(256)]

    for step in steps:
        end_of_label = 0
        for char in step:
            if char in ['-', '=']:
                break
            end_of_label += 1
        label = step[:end_of_label]
        box_number = label_hash(label)
        operation = step[end_of_label]
    
        if operation == '-':
            remove_duplicate_lens(boxes[box_number], label)
        elif operation == '=':
            focal_length = int(step[end_of_label + 1])
            set_focal_length(boxes, label, box_number, focal_length)

    total_power = calculate_power(boxes)
    return total_power

with open("2023/day-15/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    steps = parse_input(input_lines)
    assert 1320 == total_hash(steps)
    assert 145 == focusing_power(steps)

with open("2023/day-15/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    steps = parse_input(input_lines)
    print("Part 1: HASH value is ", total_hash(steps))
    print("Part 2: Focusing power is ", focusing_power(steps))
    