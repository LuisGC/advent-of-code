from typing import List

def count_fully_contained(elven_pairs: List) -> int:

    fully_contained = 0
    for pair in elven_pairs:
        first, second = pair.split(",")
        min_1, max_1 = [int(x) for x in first.split("-")]
        min_2, max_2 = [int(x) for x in second.split("-")]
        if max_1 <= max_2 and min_1 >= min_2 or max_1 >= max_2 and min_1 <= min_2:
            fully_contained += 1

    return fully_contained

def count_overlapped(elven_pairs: List) -> int:

    overlapped = 0
    for pair in elven_pairs:
        first, second = pair.split(",")
        min_1, max_1 = [int(x) for x in first.split("-")]
        min_2, max_2 = [int(x) for x in second.split("-")]
        
        sections_1 = set(list(range(min_1, max_1 + 1)))
        sections_2 = set(list(range(min_2, max_2 + 1)))
        if len(sections_1 & sections_2):
            overlapped += 1

    return overlapped


with open("2022/day-04/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 2 == count_fully_contained(input_lines)
    assert 4 == count_overlapped(input_lines)

with open("2022/day-04/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    print("Part 1: Count of fully overlapped is:", count_fully_contained(input_lines))
    print("Part 2: Count of overlapped is ", count_overlapped(input_lines))
