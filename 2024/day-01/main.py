from typing import Tuple, List

def parse_input(list: List) -> Tuple[List, List]:
    left = []
    right = []
    for line in list:
        num1, num2 = line.split("   ")
        left.append(int(num1))
        right.append(int(num2))

    left.sort()
    right.sort()

    return left, right

def total_distance(list: List) -> int:

    distance = 0
    left, right = parse_input(list)
    for i in range(len(left)):
        distance += abs(left[i] - right[i])

    return distance

def sim_score(list: List) -> int:

    score = 0
    left, right = parse_input(list)
    for i in left:
        if i in right:
            score += right.count(i) * i
            
    return score

with open("2024/day-01/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 11 == total_distance(input_lines)
    assert 31 == sim_score(input_lines)

with open("2024/day-01/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: Sum of all distances is {total_distance(input_lines)}")
    print(f"Part 2: Sum of all sim scores is {sim_score(input_lines)}")
