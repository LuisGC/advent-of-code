from typing import Tuple, List

def parse_input(input_file: str) -> Tuple[List[str], List[str]]:
    patterns, designs = input_file.split("\n\n")
    patterns = patterns.split(", ")
    designs = designs.splitlines()
    return patterns, designs

def check(design: str, patterns: List[str], checkedDesign: dict) -> int:
    if design in checkedDesign:
        return checkedDesign[design]
    
    if len(design) == 0:
        return 1
    
    options = 0
    for key in patterns:
        if design.startswith(key):
            options += check(design[len(key):], patterns, checkedDesign)
    checkedDesign[design] = options
    return options

def possible_designs(patterns: List[str], designs: List[str]) -> Tuple[int, int]:
    checkedDesign = {}
    possible = 0
    different = 0
    for design in designs:
        options = check(design, patterns, checkedDesign)
        possible += 1 if options > 0 else 0
        different += options
        
    return possible, different


with open("2024/day-19/example.txt", encoding="utf-8") as f:
    patterns, designs = parse_input(f.read())

    possible, options = possible_designs(patterns, designs)
    assert 6 == possible
    assert 16 == options

with open("2024/day-19/input.txt", encoding="utf-8") as f:
    patterns, designs = parse_input(f.read())

    possible, options = possible_designs(patterns, designs)
    print(f"Part 1: Sum of possible designs is {possible}")
    print(f"Part 2: Sum of different designs is {options}")