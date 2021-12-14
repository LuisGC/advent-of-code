from typing import List
from collections import Counter


def parse_input(input: List[str]) -> (str, dict):

    template = input[0]
    rules = {i.split(' -> ')[0] : i.split(' -> ')[1] for i in input[2:]}
    return template, rules


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


with open("2021/day-14/example.txt") as f:
    template, rules  = parse_input([line.strip() for line in f])
    assert 1588 == apply_insertion(template, rules, 10)

with open("2021/day-14/input.txt") as f:
    template, rules  = parse_input([line.strip() for line in f])
    print("Part 1: Difference between max and min occurences : ", apply_insertion(template, rules, 10))
#     print("Part 2: The alphanumeric code is : ")
#     count_dots_after_fold(paper, len(paper.fold_instructions))
