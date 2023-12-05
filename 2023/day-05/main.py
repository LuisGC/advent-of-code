import sys
from typing import Tuple, List

def parse_input (lines: list) -> Tuple[list, list]:

    seeds = [
        int(number) for number in lines[0].strip().split(": ")[-1].split()
    ]
    mappings = []
    for line in lines[1:]:
        if not line.strip():
            mappings.append([])
        elif line[0].isdigit():
            mappings[-1].append([int(number) for number in line.strip().split()])

    return seeds, mappings

def find_lowest_location(seeds: List[int], mappings: List[int]) -> int:
    lowest = sys.maxsize

    for seed in seeds:
        for mapping in mappings:
            for destination_start, source_start, range_length in mapping:
                source_end = source_start + range_length

                if source_start <= seed <= source_end:
                    seed = (seed - source_start) + destination_start
                    break
                
        lowest = min(lowest, seed)

    return lowest


with open("2023/day-05/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    seeds, mappings = parse_input(input_lines)
    
    assert 35 == find_lowest_location(seeds, mappings)

with open("2023/day-05/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    seeds, mappings = parse_input(input_lines)
    
    print("Part 1: Lowest location is ", find_lowest_location(seeds, mappings))
    # print("Part 2: Sum of all gear ratios is ", sum_all_gear_ratios)
