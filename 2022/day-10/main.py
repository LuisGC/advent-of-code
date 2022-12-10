from typing import List

def parse_input(lines: List) -> List:
    instructions = []
    for line in lines:
        parts = line.split()
        if parts[0] == "noop":
            instructions.append((parts[0], 0))
        else: # addx
            instructions.append((parts[0], int(parts[1])))

    return instructions

def execute_instructions(instructions: List, show_signal:bool=True) -> int:
    MEASURE_CYCLES = [20, 60, 100, 140, 180, 220]
    signal_strenght = 0
    x_register = 1
    queued_instructions = None
    instructions_iterator = iter(instructions)
    crt_line = ""

    for cycle in range(1, 241):
        # measure if needed
        if cycle in MEASURE_CYCLES:
            signal_strenght += cycle * x_register

        if abs(((cycle - 1) % 40) - x_register) <= 1:
            crt_line += "#"
        else:
            crt_line += "."

        if show_signal and cycle % 40 == 0:
            print(crt_line)
            crt_line = ""

        if queued_instructions:
            x_register += queued_instructions
            queued_instructions = None
        else:
            instruction = next(instructions_iterator)

            if instruction[0] == "noop":
                continue
            else:
                queued_instructions = instruction[1]

    # print(signal_strenght)
    return signal_strenght


with open("2022/day-10/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    instructions = parse_input(input_lines)

    assert 13140 == execute_instructions(instructions, False)

with open("2022/day-10/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    instructions = parse_input(input_lines)

    print("Part 1: total signal strenght is:", execute_instructions(instructions))
