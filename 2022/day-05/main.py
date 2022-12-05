from typing import List

def execute_instructions(lines: List) -> str:
    split_pos = next(i for i, line in enumerate(lines) if "1" in line)

    stacks= [[], [], [], [], [], [], [], [], []]
    for line in reversed(lines[:split_pos]):
        for i, crate in enumerate(line[1::4]):
            if crate != " ":
                stacks[i].append(crate)

    instructions = [[int(x) for x in line.replace("move ", "").replace(" from ", ",").replace(" to ", ",").split(",")] for line in lines[split_pos + 2:]]

    for (amount, source, dest) in (instructions):
        # print(stacks)
        for i in range(amount):
            stacks[dest - 1].extend(stacks[source - 1][-1:])
            stacks[source - 1] = stacks[source - 1][:-1]

    # print(stacks)
    return "".join(stack[-1] for stack in stacks if stack)

with open("2022/day-05/example.txt", encoding="utf-8") as f:
    
    assert "CMZ" == execute_instructions(f.readlines())

with open("2022/day-05/input.txt", encoding="utf-8") as f:
    print("Part 1: Final crates on top are :", execute_instructions(f.readlines()))
