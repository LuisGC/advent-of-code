import sys
from typing import Tuple, List

def parse_input (lines: List[str]) -> Tuple[List[int], List[int]]:

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

def find_lowest_location_with_ranges(seeds: List[int], mappings: List[int]) -> int:
    seed_ranges = [
        (start, start + length) for start, length in zip(seeds[0::2], seeds[1::2])
    ]
    candidates = [[] for _ in range(len(mappings))]

    for range_start, range_end in seed_ranges:
        ranges = [(range_start, range_end)]

        for i, mapping in enumerate(mappings):
            while ranges:
                range_start, range_end = ranges.pop()

                for destination_start, source_start, range_length in mapping:
                    source_end = source_start + range_length
                    offset = destination_start - source_start

                    if source_end <= range_start or range_end <= source_start:
                        continue

                    if range_start < source_start:
                        ranges.append((range_start, source_start))
                        range_start = source_start

                    if source_end < range_end:
                        ranges.append((source_end, range_end))
                        range_end = source_end
                    
                    range_start += offset
                    range_end += offset

                    break
                
                candidates[i].append((range_start, range_end))

            ranges = candidates[i]

    return min(candidates[-1])[0]


with open("2023/day-05/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    seeds, mappings = parse_input(input_lines)
    
    assert 35 == find_lowest_location(seeds, mappings)
    assert 46 == find_lowest_location_with_ranges(seeds, mappings)

with open("2023/day-05/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    seeds, mappings = parse_input(input_lines)
    
    print("Part 1: Lowest location is ", find_lowest_location(seeds, mappings))
    print("Part 2: Lowest location with seed ranges is ", find_lowest_location_with_ranges(seeds, mappings))
