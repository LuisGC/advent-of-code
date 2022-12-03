from typing import List

alphabet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def missplaced_priority(rucksack_list: List) -> int:
    priority = 0
    for rucksack in rucksack_list:
        comp_1 = rucksack[:len(rucksack) // 2]
        comp_2 = rucksack[-len(rucksack) // 2:]
        missplaced = set([item for item in comp_1]) & set([item for item in comp_2])
        priority += alphabet.index(list(missplaced)[0])
        
    return priority
    
def common_badge_priority(rucksack_list: List) -> int:
    priority = 0
    for index in range(len(rucksack_list)):
        if index % 3 == 0:
            common_badge = set([item for item in rucksack_list[index]]) & set([item for item in rucksack_list[index + 1]]) & set([item for item in rucksack_list[index + 2]])
            priority += alphabet.index(list(common_badge)[0])

    return priority


with open("2022/day-03/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 157 == missplaced_priority(input_lines)
    assert 70 == common_badge_priority(input_lines)

with open("2022/day-03/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    print("Part 1: Priority of the missplaced items is:", missplaced_priority(input_lines))
    print("Part 2: Priority of the common badges is ", common_badge_priority(input_lines))
