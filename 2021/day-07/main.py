from typing import List


def consumption(baseline: int, pos: int) -> int:
    return abs(baseline - pos)


def incremental_consumption(baseline: int, pos: int) -> int:
    distance = abs(baseline - pos)
    return int(distance * (distance + 1) / 2)


def align_crabs(positions: List[int]) -> (int, int):

    fuel_constant = 10**10
    fuel_incremental = 10**10

    for baseline in range(min(positions), max(positions)):
        current_fuel_constant = 0
        current_fuel_incremental = 0
        for pos in positions:
            current_fuel_constant += consumption(baseline, pos)
            current_fuel_incremental += incremental_consumption(baseline, pos)

        fuel_constant = min(fuel_constant, current_fuel_constant)
        fuel_incremental = min(fuel_incremental, current_fuel_incremental)

    return fuel_constant, fuel_incremental


with open("2021/day-07/example.txt") as f:
    input = [int(num) for num in f.readline().strip().split(',')]
    fuel_constant, fuel_incremental = align_crabs(input)
    assert 37 == fuel_constant
    assert 168 == fuel_incremental


with open("2021/day-07/input.txt") as f:
    input = [int(num) for num in f.readline().strip().split(',')]

    fuel_constant, fuel_incremental = align_crabs(input)
    print("Part 1: The amount of fuel is", fuel_constant)
    print("Part 2: The amount of fuel is", fuel_incremental)
