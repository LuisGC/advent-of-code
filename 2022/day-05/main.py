from typing import List

def execute_instructions(lines: List, crate_mover: int=9000) -> str:
    split_pos = next(i for i, line in enumerate(lines) if "1" in line)

    stacks= [[], [], [], [], [], [], [], [], []]
    for line in reversed(lines[:split_pos]):
        for i, crate in enumerate(line[1::4]):
            if crate != " ":
                stacks[i].append(crate)

    instructions = [[int(x) for x in line.replace("move ", "").replace(" from ", ",").replace(" to ", ",").split(",")] for line in lines[split_pos + 2:]]

    for (amount, source, dest) in (instructions):
        # print(stacks)
        if crate_mover == 9000:
            for i in range(amount):
                stacks[dest - 1].extend(stacks[source - 1][-1:])
                stacks[source - 1] = stacks[source - 1][:-1]
        else:
            stacks[dest - 1].extend(stacks[source - 1][-amount:])
            stacks[source - 1] = stacks[source - 1][:-amount]


    # print(stacks)
    return "".join(stack[-1] for stack in stacks if stack)

with open("2022/day-05/example.txt", encoding="utf-8") as f:
    lines = f.readlines()
    assert "CMZ" == execute_instructions(lines)
    assert "MCD" == execute_instructions(lines, 9001)

with open("2022/day-05/input.txt", encoding="utf-8") as f:
    lines = f.readlines()
    print("Part 1: Final crates on top with CrateMover 9000 are :", execute_instructions(lines))
    print("Part 2: Final crates on top with CrateMover 9001 are :", execute_instructions(lines, 9001))
