from __future__ import annotations
from typing import NamedTuple, List


class Command (NamedTuple):
    operation: str
    units: int

    @staticmethod
    def parse(line: str) -> Command:
        op, arg = line.strip().split()
        return Command(op, int(arg))


def run_commands(commands: List[Instruction]) -> int:
    horizontal = 0
    depth = 0

    for command in commands:
        if command.operation == 'forward':
            horizontal += command.units
        elif command.operation == 'down':
            depth += command.units
        else:
            depth -= command.units

    return horizontal * depth


def run_commands_aim(commands: List[Instruction]) -> int:
    horizontal = 0
    depth = 0
    aim = 0

    for command in commands:
        if command.operation == 'forward':
            horizontal += command.units
            depth += aim * command.units
        elif command.operation == 'down':
            aim += command.units
        else: # "up"
            aim -= command.units

    print(horizontal, depth)
    return horizontal * depth



with open("2021/day-02/example.txt", encoding="utf-8") as f:
    code = f.read().strip()
    commands = [Command.parse(line) for line in code.split("\n")]
    assert 150 == run_commands(commands)
    assert 900 == run_commands_aim(commands)


with open("2021/day-02/input.txt", encoding="utf-8") as f:
    code = f.read().strip()
    commands = [Command.parse(line) for line in code.split("\n")]
    print("Part 1: distance * depth is", run_commands(commands))
    print("Part 2: distance * depth with aim is", run_commands_aim(commands))
