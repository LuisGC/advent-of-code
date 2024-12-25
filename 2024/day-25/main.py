from typing import Tuple, List

def parse_input(input: List[str]) -> Tuple[List[str], List[str]]:
    locks = []
    keys = []
    for block in input:
        block = block.splitlines()
        heigths = [sum(1 for row in range(1, 6) if block[row][col] == "#") for col in range(5)]

        if block[0][0] == "#":
            locks.append(heigths)
        else:
            keys.append(heigths)

    return locks, keys

def can_fit(key: List[int], lock: List[int]) -> bool:
    return not any(k + l > 5 for k, l in zip(key, lock))

def find_matches(locks: List[List[int]], keys: List[List[int]]) -> int:
    matches = 0
    for key in keys:
        for lock in locks:
            if can_fit(key, lock):
                matches += 1
    return matches


with open("2024/day-25/example.txt", encoding="utf-8") as f:
    locks, keys = parse_input(f.read().split("\n\n"))
    
    assert 3 == find_matches(locks, keys)

with open("2024/day-25/input.txt", encoding="utf-8") as f:
    locks, keys = parse_input(f.read().split("\n\n"))

    print(f"Part 1: Sum of possible matches is {find_matches(locks, keys)}")