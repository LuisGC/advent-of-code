from typing import List


def consumption(baseline: int, pos: int) -> int:
    return abs(baseline - pos)


def incremental_consumption(baseline: int, pos: int) -> int:
    distance = abs(baseline - pos)
    return int(distance * (distance + 1) / 2)


def align_crabs(positions: List[int], constant_rate: bool) -> int:

    fuel = 10**10

    for baseline in range(min(positions), max(positions)):
        current_fuel = 0
        for pos in positions:
            if constant_rate:
                current_fuel += consumption(baseline, pos)
            else:
                current_fuel += incremental_consumption(baseline, pos)

        fuel = min(fuel, current_fuel)

    return fuel


with open("2021/day-07/example.txt") as f:
    input = [int(num) for num in f.readline().strip().split(',')]
    assert 37 == align_crabs(input, True)
    assert 168 == align_crabs(input, False)


with open("2021/day-07/input.txt") as f:
    input = [int(num) for num in f.readline().strip().split(',')]

    print("Part 1: The amount of fuel is", align_crabs(input, True))
    print("Part 2: The amount of fuel is", align_crabs(input, False))
