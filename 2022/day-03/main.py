from typing import List

alphabet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def calculate_priorities(input_lines: List) -> int:
    priorities = 0
    for rucksack in input_lines:
        comp_1 = rucksack[:len(rucksack) // 2]
        comp_2 = rucksack[-len(rucksack) // 2:]
        missplaced = set([item for item in comp_1]) & set([item for item in comp_2])
        priorities += alphabet.index(list(missplaced)[0])
        
    return priorities
    

with open("2022/day-03/example.txt") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 157 == calculate_priorities(input_lines)
    
    # cheat_plays = decrypt_plays(clean_plays)
    # assert 12 == calculate_priorities(cheat_plays)


with open("2022/day-03/input.txt") as f:
    input_lines = [line.strip() for line in f.readlines()]
    print("Part 1: The sum of priorities is:", calculate_priorities(input_lines))

#     cheat_plays = decrypt_plays(clean_plays)
#     calculate_priorities(cheat_plays)
#     print("Part 2: Score applying strategy is ", calculate_priorities(cheat_plays))

