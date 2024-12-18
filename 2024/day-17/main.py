from typing import List, Tuple
import re

def parse_input(lines: List[str]) -> Tuple[List[int], dict]:
    input = re.compile("(\d+)")
    registers = {}
    registers["A"] = int(input.search(lines[0]).group(0))
    registers["B"] = int(input.search(lines[1]).group(0))
    registers["C"] = int(input.search(lines[2]).group(0))

    program = list(map(int, input.findall(lines[4])))

    return program, registers

def run_program(program: List[int], registers: dict) -> str:
    output = []
    pointer = 0
    while True:
        op_code = program[pointer]
        combo_op = program[pointer + 1]
        pointer += 2

        pointer, registers = execute(op_code, combo_op, output, registers, pointer)
        if pointer == -1:
            break

    return ",".join(str(x) for x in output)

def execute(op_code: int, combo_op: int, output: List[int], registers: dict, pointer: int) -> Tuple[int, dict]:
    op_value = combo_op_value(combo_op, registers)

    if op_code == 0:
        registers["A"] = registers["A"] // (2 ** op_value)
    elif op_code == 1:
        registers["B"] = registers["B"] ^ combo_op
    elif op_code == 2:
        registers["B"] = op_value % 8
    elif op_code == 3:
        pointer = -1 if registers["A"] == 0 else op_value
    elif op_code == 4:
        registers["B"] = registers["B"] ^ registers["C"]
    elif op_code == 5:
        output.append(op_value % 8)
    elif op_code == 6:
        registers["B"] = registers["A"] // (2 ** op_value)
    elif op_code == 7:
        registers["C"] = registers["A"] // (2 ** op_value)
    else:
        raise Exception
    
    return pointer, registers

def combo_op_value(combo_op: int, registers: dict) -> int:
    if combo_op < 4:
        return combo_op
    elif combo_op == 4:
        return registers["A"]
    elif combo_op == 5:
        return registers["B"]
    elif combo_op == 6:
        return registers["C"]


with open("2024/day-17/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    program, registers = parse_input(input_lines)

    assert "4,6,3,5,6,3,5,2,1,0" == run_program(program, registers)

with open("2024/day-17/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    program, registers = parse_input(input_lines)

    print(f"Part 1: Output of the program is {run_program(program, registers)}")