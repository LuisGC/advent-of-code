from __future__ import annotations
from typing import NamedTuple, List


class Instruction (NamedTuple):
    operation: str
    argument: int

    @staticmethod
    def parse(line: str) -> Instruction:
        op, arg = line.strip().split()
        return Instruction(op, int(arg))


def run_until_loop(instructions: List[Instruction]) -> int:
    accumulator = 0
    pc = 0
    executed = []
    finished = False

    while pc not in executed and pc < len(instructions):
        executed.append(pc)
        if instructions[pc].operation == 'nop':
            pc += 1
        elif instructions[pc].operation == 'acc':
            accumulator += instructions[pc].argument
            pc += 1
        elif instructions[pc].operation == 'jmp':
            pc += instructions[pc].argument
        else:
            finished = True

    return accumulator, finished or pc == len(instructions), executed


def fix_program(instructions: List[Instruction],
                line_to_fix: int) -> List[Instruction]:
    fixed_program = instructions.copy()
    if fixed_program[line_to_fix].operation == 'nop':
        fixed_program[line_to_fix] = Instruction('jmp', fixed_program[line_to_fix].argument)
    elif fixed_program[line_to_fix].operation == 'jmp':
        fixed_program[line_to_fix] = Instruction('nop', fixed_program[line_to_fix].argument)

    return fixed_program


def run_removing_loops(instructions: List[Instruction]) -> int:
    accumulator, finished, executed = run_until_loop(instructions)
    i = 0

    while not finished and executed[i] < len(instructions) and i < len(executed):
        fixed_program = fix_program(instructions, executed[i])
        accumulator, finished, executed_fixed = run_until_loop(fixed_program)
        i += 1

    return accumulator


with open("2020/day-08/example.txt") as f:
    code = f.read().strip()
    instructions = [Instruction.parse(line) for line in code.split("\n")]
    assert 5 == run_until_loop(instructions)[0]
    assert 8 == run_removing_loops(instructions)


with open("2020/day-08/input.txt") as f:
    code = f.read().strip()
    instructions = [Instruction.parse(line) for line in code.split("\n")]
    print("Part 1: Accumulator is", run_until_loop(instructions)[0])
    print("Part 2: Removing loops, accumulator is",
          run_removing_loops(instructions))
