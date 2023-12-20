from typing import List, Tuple, Mapping, Dict
from time import perf_counter

ACCEPTED = "A"
REJECTED = "R"

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took: " + "{:2.5f}".format(perf_counter() - t) + " sec") 
        return ret
    
    return wrapper_method

def parse_input(blocks: List[str]) -> Tuple[dict, List[Mapping]]:
    workflows = {}
    for line in blocks[0].split("\n"):
        label, rules_block = line[:-1].split("{")
        rules = rules_block.split(",")
        workflows[label] = [rule.split(":") for rule in rules[:-1] + [rules[-1]]]

    part_ratings = []
    for line in blocks[1].split("\n"):
        rating = {}
        for item in line[1:-1].split(","):
            key, value = item.split("=")
            rating[key] = int(value)
        part_ratings.append(rating)

    return workflows, part_ratings

def part_is_accepted(workflows: dict, part: Mapping[str, int]) -> int:
    current = "in"

    while current not in [ACCEPTED, REJECTED]:
        rules = workflows[current]
        for rule, next in rules[:-1]:
            if rule[1] == "<":
                letter, value = rule.split("<")
                if part[letter] < int(value):
                    current = next
                    break
            elif rule[1] == ">":
                letter, value = rule.split(">")
                if part[letter] > int(value):
                    current = next
                    break
        else:
            current = rules[-1][0]

    return current == ACCEPTED

@profiler
def process_parts(workflows: dict, part_ratings: List[Mapping]) -> int:
    total = 0
    for part in part_ratings:
        if part_is_accepted(workflows, part):
            total += sum(part.values())

    return total

def solve(workflows: dict, valid_ranges: Dict[str, Tuple[int, int]], current: str, valid_solutions: List[Dict]):

    if current == REJECTED:
        return
    if current == ACCEPTED:
        valid_solutions.append(valid_ranges)
        return
    
    for rule, next in workflows[current][:-1]:
        if rule[1] == "<":
            ranges_copy = valid_ranges.copy()
            letter, value = rule.split("<")
            old = ranges_copy[letter]
            ranges_copy[letter] = old[0], min(int(value) - 1, old[1])

            valid_ranges[letter] = int(value), old[1]
            solve(workflows, ranges_copy, next, valid_solutions)

        elif rule[1] == ">":
            ranges_copy = valid_ranges.copy()
            letter, value = rule.split(">")
            old = ranges_copy[letter]
            ranges_copy[letter] = max(int(value) + 1, old[0]), old[1]

            valid_ranges[letter] = old[0], int(value)
            solve(workflows, ranges_copy, next, valid_solutions)
    
    solve(workflows, valid_ranges, workflows[current][-1][0], valid_solutions)

@profiler
def valid_ranges(workflows: dict) -> int:
    total = 0
    ranges = {letter: (1, 4000) for letter in "xmas"}
    valid_solutions = []
    solve(workflows, ranges, "in", valid_solutions)

    for solution in valid_solutions:
        value = 1
        for lower, upper in solution.values():
            value *= upper - lower + 1
        total += value

    return total


with open("2023/day-19/example.txt", encoding="utf-8") as f:
    blocks = f.read().strip().split("\n\n")
    workflows, part_ratings = parse_input(blocks)

    assert 19114 == process_parts(workflows, part_ratings)
    assert 167409079868000 == valid_ranges(workflows)

with open("2023/day-19/input.txt", encoding="utf-8") as f:
    blocks = f.read().strip().split("\n\n")
    workflows, part_ratings = parse_input(blocks)
    
    print("Part 1: The sum of all accepted part_ratings is ", process_parts(workflows, part_ratings))
    print("Part 2: The sum of all valid ranges is ", valid_ranges(workflows))