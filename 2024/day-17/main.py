from typing import List, Tuple, Iterator
import re

def parse_input(lines: List[str]) -> Tuple[List[int], List[int]]:
    input = re.compile("(\d+)")
    registers = []
    registers.append(int(input.search(lines[0]).group(0)))
    registers.append(int(input.search(lines[1]).group(0)))
    registers.append(int(input.search(lines[2]).group(0)))

    program = list(map(int, input.findall(lines[4])))

    return program, registers

def run_program(program: List[int], registers: List[int]) -> str:
    output = []
    pointer = 0
    
    while pointer < len(program):
        op_code = program[pointer]
        combo_op = program[pointer + 1]
        pointer += 2

        pointer, registers = execute(op_code, combo_op, output, registers, pointer)

    return output

def execute(op_code: int, combo_op: int, output: List[int], registers: List[int], pointer: int) -> Tuple[int, dict]:
    op_value = combo_op_value(combo_op, registers)

    if op_code == 0:
        registers[0] = registers[0] // (2 ** op_value)
    elif op_code == 1:
        registers[1] = registers[1] ^ combo_op
    elif op_code == 2:
        registers[1] = op_value % 8
    elif op_code == 3:
        if registers[0] != 0:
            pointer = op_value
    elif op_code == 4:
        registers[1] = registers[1] ^ registers[2]
    elif op_code == 5:
        output.append(op_value % 8)
    elif op_code == 6:
        registers[1] = registers[0] // (2 ** op_value)
    elif op_code == 7:
        registers[2] = registers[0] // (2 ** op_value)
    else:
        raise ValueError(f"Unknown op_code {op_code}")
    
    return pointer, registers

def combo_op_value(combo_op: int, registers: List[int]) -> int:
    if combo_op < 4:
        return combo_op
    elif combo_op == 4:
        return registers[0]
    elif combo_op == 5:
        return registers[1]
    elif combo_op == 6:
        return registers[2]

def lowest_register(program: List[int], registers: List[int], remaining_digits: int) -> int:

    reg_a, reg_b, reg_c = registers

    if remaining_digits < 0:
        return reg_a
    
    for i in range(8):
        candidate_a = reg_a * 8 + i
        result = run_program(program, [candidate_a, reg_b, reg_c])
        expected_digit = program[remaining_digits]

        if int(result[0]) == expected_digit:
            result = lowest_register(program, [candidate_a, reg_b, reg_c], remaining_digits - 1)
            if result is not None:
                return result
        
    return None # No solution found


with open("2024/day-17/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    program, registers = parse_input(input_lines)

    output = run_program(program, registers)
    assert [4,6,3,5,6,3,5,2,1,0] == output

with open("2024/day-17/example-2.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    program, registers = parse_input(input_lines)

    output = run_program(program, registers)
    assert 117440 == lowest_register(program, registers, len(program) - 1)

with open("2024/day-17/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    program, registers = parse_input(input_lines)

    print(f"Part 1: Output of the program is {run_program(program, registers)}")
    print(f"Part 2: Lowest value of A register is {lowest_register(program, registers, len(program) - 1)}")