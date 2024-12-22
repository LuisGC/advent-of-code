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
    while pointer < len(program):
        op_code = program[pointer]
        combo_op = program[pointer + 1]
        pointer += 2

        pointer, registers = execute(op_code, combo_op, output, registers, pointer)

    return output

def execute(op_code: int, combo_op: int, output: List[int], registers: dict, pointer: int) -> Tuple[int, dict]:
    op_value = combo_op_value(combo_op, registers)

    if op_code == 0:
        registers["A"] = registers["A"] // (2 ** op_value)
    elif op_code == 1:
        registers["B"] = registers["B"] ^ combo_op
    elif op_code == 2:
        registers["B"] = op_value % 8
    elif op_code == 3:
        if registers["A"] != 0:
            pointer = op_value
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

def lowest_register_a(program: List[int], iteration: int = 0, prev_a: int = 0) -> int:
    if iteration == len(program):
        return prev_a
    
    for i in range(8):
        output = []
        pointer = 0
        start_a = prev_a * 8 + i
        registers = {}
        registers["A"] = start_a
        registers["B"] = 0
        registers["C"] = 0

        while True:
            op_code = program[pointer]
            combo_op = program[pointer + 1]
            pointer += 2

            if op_code == 3:
                break

            pointer, registers = execute(op_code, combo_op, output, registers, pointer)

        if output[0] == program[-(iteration + 1)]:
            res = lowest_register_a(program, iteration + 1, start_a)
            if res is None: continue
            registers["A"] = res
            output = run_program(program, registers)
            if program != output:
                continue
            return res

def lowest_register(program: List[int], iteration: int, value: int = 0) -> int:
    for addition in range(8):
        registers = {}
        registers["A"] = value * 8 + addition
        registers["B"] = 0
        registers["C"] = 0

        output = run_program(program, registers)
        if output == program[iteration:]:
            if iteration == 0:
                return 8 * value + addition
            best = lowest_register(program, iteration - 1, 8 * value + addition)
            if best is not None:
                return best
    return None


with open("2024/day-17/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    program, registers = parse_input(input_lines)

    output = run_program(program, registers)
    assert [4,6,3,5,6,3,5,2,1,0] == output

    assert 117440 == lowest_register_a(program)

with open("2024/day-17/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    program, registers = parse_input(input_lines)

    print(f"Part 1: Output of the program is {run_program(program, registers)}")
    print(f"Part 2: Lowest value of A register is {lowest_register_a(program)}")