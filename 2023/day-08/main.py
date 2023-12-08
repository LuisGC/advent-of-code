from typing import List
import re

def parse_input (lines: List[str]) -> dict:
    nodes = {
        x[1]: (x[2], x[3])
        for x in (re.match(r"(\w+)\s*=\s*\((\w+), (\w+)\)", line) for line in lines)
    }
    return nodes

def steps_required(instructions: str, nodes: dict) -> int:
    next_node = "AAA"
    last_node = "ZZZ"

    i = 0
    steps = 0

    while next_node != last_node:
        if i >= len(instructions):
            i = 0

        instruction = instructions[i]
        node = nodes[next_node]
        next_node = node[instruction == "R"]

        steps += 1
        i += 1

    return steps

with open("2023/day-08/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    instructions = input_lines[0]
    nodes = parse_input(input_lines[2:])

    assert 2 == steps_required(instructions, nodes)
    

with open("2023/day-08/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    instructions = input_lines[0]
    nodes = parse_input(input_lines[2:])

    print("Part 1: Total steps required are ", steps_required(instructions, nodes))
#    print("Part 2: Total winnings with Jokers are ", total_winnings(hands, jokers=True))
