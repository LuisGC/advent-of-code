from typing import List

def parse_adapters(input : str) -> List[int]:
    adapters = []
    for line in input:
        adapters.append(int(line))

    adapters.append(max(adapters)+3) # the built-in adapter

    adapters.sort()
    return adapters

def find_yolt_gaps (adapters: List[int]) -> [int, int]:

    yolts = 0
    gaps_1 = 0
    gaps_3 = 0

    for item in adapters:
        if int(item) - yolts == 3:
            gaps_3 += 1
        elif int(item) - yolts == 1:
            gaps_1 += 1

        yolts = item

    return gaps_1, gaps_3

def count_arrangements(adapters: List[int]) -> int:
    return 8

with open("day-10/example.txt") as f:
    adapters = parse_adapters(f.readlines())
    gaps_1, gaps_3 = find_yolt_gaps(adapters)
    assert 35 == gaps_1 * gaps_3

with open("day-10/large-example.txt") as f:
    adapters = parse_adapters(f.readlines())
    gaps_1, gaps_3 = find_yolt_gaps(adapters)
    assert 220 == gaps_1 * gaps_3

with open("day-10/input.txt") as f:
    adapters = parse_adapters(f.readlines())
    gaps_1, gaps_3 = find_yolt_gaps(adapters)
    print("Part 1: The 1&3 yolt gaps multiplied is", gaps_1 * gaps_3)
