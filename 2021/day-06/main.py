from typing import List


def step(counts: List[int]) -> List[int]:
    new_counts = [0] * 9
    new_counts[6] = new_counts[8] = counts[0]
    for i in range(8):
        new_counts[i] += counts[i + 1]
    return new_counts


def count_fish(input: str, days: int) -> int:
    counts = [input.count(str(i)) for i in range(9)]
    for item in range(days):
        counts = step(counts)

    return sum(counts)


with open("2021/day-06/example.txt") as f:
    input = f.readline()

    assert 26 == count_fish(input, 18)
    assert 5934 == count_fish(input, 80)
    assert 26984457539 == count_fish(input, 256)


with open("2021/day-06/input.txt") as f:
    input = f.readline()
    print("Part 1: The amount of lanternfish is", count_fish(input, 80))
    print("Part 2: The amount of lanternfish is", count_fish(input, 256))
