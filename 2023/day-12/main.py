from functools import cache
from typing import List, Tuple

def parse_input (lines: List[str]) -> List[Tuple[str, List[int]]]:
    rows = []
    for line in lines:
        pattern, splits = line.split()
        splits = tuple(int(number) for number in splits.split(","))
        rows.append([pattern, splits])
    return rows

@cache
def count_permutations(pattern: str, splits: List[int]) -> int:
    if len(splits) == 0:
        if all(char in '.?' for char in pattern):
            return 1
        else:
            return 0

    current_split, remaining_splits = splits[0], splits[1:]
    after = sum(remaining_splits) + len(remaining_splits)

    count = 0
    for before in range(len(pattern) - after - current_split + 1):
        candidate = '.' * before + '#' * current_split + '.'
        if all(char_1 == '?' or char_1 == char_2 for char_1, char_2 in zip(pattern, candidate)):
            count += count_permutations(pattern[len(candidate):], remaining_splits)
    return count

def sum_all_permutations(rows: List, unfolding: bool = False) -> int:
    count = 0
    for pattern, splits in rows:
        if unfolding:
            pattern = '?'.join((pattern,) * 5)
            splits = splits * 5
        count += count_permutations(pattern, splits)
    return count


with open("2023/day-12/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    rows = parse_input(input_lines)

    assert 21 == sum_all_permutations(rows)
    assert 525152 == sum_all_permutations(rows, unfolding=True)

with open("2023/day-12/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    rows = parse_input(input_lines)
    
    print("Part 1: The sum of all options is ", sum_all_permutations(rows))
    print("Part 2: The sum of all options after unfolding is ", sum_all_permutations(rows, unfolding=True))
