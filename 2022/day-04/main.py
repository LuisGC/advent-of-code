from typing import List

def count_fully_contained(elven_pairs: List) -> int:

    fully_contained = 0
    for pair in elven_pairs:
        first, second = pair.split(",")
        first_min, first_max = first.split("-")
        second_min, second_max = second.split("-")
        if int(first_max) <= int(second_max) and int(first_min) >= int(second_min) or int(first_max) >= int(second_max) and int(first_min) <= int(second_min):
            fully_contained += 1

    return fully_contained

with open("2022/day-04/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 2 == count_fully_contained(input_lines)
    # assert 70 == common_badge_priority(input_lines)

with open("2022/day-04/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    print("Part 1: Count of fully overlapped is:", count_fully_contained(input_lines))
#     print("Part 2: Priority of the common badges is ", common_badge_priority(input_lines))
