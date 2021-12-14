from typing import List
from collections import Counter
import sys

def parse_input(input: List[str]) -> (str, dict):

    template = input[0]
    rules = {i.split(' -> ')[0] : i.split(' -> ')[1] for i in input[2:]}
    return template, rules


def replace_pair(pairs: List[str], rules: dict) -> str:
    new = template[0]
    for pair in pairs:
        if pair in rules:
            new += rules[pair] + pair[1]
        else:
            new += pair[1]
    return new


def apply_insertion(template: str, rules: dict, steps: int) -> int:

    for step in range(steps):
        pairs = [template[i] + template[i + 1] for i in range(0, len(template) - 1)]
        new = template[0]
        for pair in pairs:
            if pair in rules:
                new += rules[pair] + pair[1]
            else:
                new += pair[1]
        template = new

    c = Counter(template)

    return (max(c.values()) - min(c.values()))


def count_replacements(template: str, rules: dict, steps: int) -> int:

    pair_count = {}

    for i in range(len(template) - 1):
        pair = template[i:i+2]
        pair_count[pair] = pair_count.get(pair, 0) + 1

    for step in range(steps):
        new_pair_count = {}
        for (pair, count) in pair_count.items():
            if pair in rules:
                new_char = rules[pair]
                new_pair1 = pair[0] + new_char
                new_pair2 = new_char + pair[1]
                new_pair_count[new_pair1] = new_pair_count.get(new_pair1, 0) + count
                new_pair_count[new_pair2] = new_pair_count.get(new_pair2, 0) + count
            else:
                new_pair_count[pair] = count
        pair_count = new_pair_count

    sum = 0
    counts = {
        template[-1] : 1
    }
    for pair, count in pair_count.items():
        counts[pair[0]] = counts.get(pair[0], 0) + count
        sum += count

    c = Counter(counts)

    return max(c.values()) - min(c.values())


with open("2021/day-14/example.txt") as f:
    template, rules  = parse_input([line.strip() for line in f])
    assert 1588 == apply_insertion(template, rules, 10)
    assert 1588 == count_replacements(template, rules, 10)
    assert 2188189693529 == count_replacements(template, rules, 40)

with open("2021/day-14/input.txt") as f:
    template, rules  = parse_input([line.strip() for line in f])
    print("Part 1: Difference between max and min occurences:", apply_insertion(template, rules, 10))
    print("Part 2: With 40 steps, difference is:", count_replacements(template, rules, 40))

# 1976896901756
