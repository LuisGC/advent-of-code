import functools
import sys
sys.path.insert(0, './')
from utils import profiler

@functools.lru_cache(maxsize=None)
def stones_produced_by_stone(stone: int, num_of_blinks: int) -> int:

    assert num_of_blinks >= 0
    if num_of_blinks == 0:
        return 1
    if stone == 0:
        return stones_produced_by_stone(1, num_of_blinks - 1)
    
    stone_as_str = str(stone)
    if len(stone_as_str) % 2 == 0:
        left = int(stone_as_str[0 : len(stone_as_str) // 2])
        right = int(stone_as_str[len(stone_as_str) // 2 :])
        return stones_produced_by_stone(left, num_of_blinks - 1) + stones_produced_by_stone(right, num_of_blinks - 1)

    return stones_produced_by_stone(2024 * stone, num_of_blinks - 1)

@profiler
def stones_produced(stones: list[int], num_of_blinks: int) -> int:
    return sum(stones_produced_by_stone(_, num_of_blinks) for _ in stones)

with open("2024/day-11/example.txt", encoding="utf-8") as f:
    rocks = [int(_) for _ in f.read().split()]
    assert 7 == stones_produced(rocks, 1)

with open("2024/day-11/example-2.txt", encoding="utf-8") as f:
    rocks = [int(_) for _ in f.read().split()]
    assert 3 == stones_produced(rocks, 1)
    assert 4 == stones_produced(rocks, 2)
    assert 5 == stones_produced(rocks, 3)
    assert 9 == stones_produced(rocks, 4)
    assert 13 == stones_produced(rocks, 5)
    assert 22 == stones_produced(rocks, 6)
    assert 55312 == stones_produced(rocks, 25)

with open("2024/day-11/input.txt", encoding="utf-8") as f:
    rocks = [int(_) for _ in f.read().split()]

    print(f"Part 1: Amount of rocks after 25 blinks is {stones_produced(rocks, 25)}")
    print(f"Part 2: Amount of rocks after 75 blinks is {stones_produced(rocks, 75)}")
