from typing import List

def parse_input (lines: List[str]) -> List[List[int]]:
    return [[int(num) for num in line.split(" ")] for line in lines]

def next_value(sequence: List[int]) -> int:
    if sequence == [0 for i in range(len(sequence))]:
        return 0
    
    new_sequence = []
    for i in range(len(sequence) - 1):
        new_sequence.append(sequence[i+1] - sequence[i])

    return sequence[-1] + next_value(new_sequence)

def extrapolate_values(sequences: List[List[int]]) -> List[int]:
    next_values = []
    for seq in sequences:
        next_values.append(next_value(seq))
    return next_values

with open("2023/day-09/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    sequences = parse_input(input_lines)

    assert 114 == sum(extrapolate_values(sequences))
    
with open("2023/day-09/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    sequences = parse_input(input_lines)

    print("Part 1: The sum of extrapolated values is ", sum(extrapolate_values(sequences)))

