from typing import Dict, List
from collections import defaultdict


def to_binary(value: int, num_digits: int = 36) -> List[int]:
    digits = []
    for _ in range(num_digits):
        digits.append(value % 2)
        value = value // 2
    return list(reversed(digits))


def apply_mask2(value: int, mask: str) -> int:
    digits = to_binary(value)

    for i, (digit, m) in enumerate(zip(digits, mask)):
        if m == '1':
            digits[i] = 1
        elif m == '0':
            digits[i] = 0

    return sum(digit * (2 ** i) for i, digit in enumerate(reversed(digits)))


def initialize(program: List[str]) -> Dict[int, int]:
    memory = defaultdict(int)
    mask = None

    for line in program:
        if line.startswith("mask"):
            mask = line.split(" = ")[-1]
        else:
            mem, value_s = line.split(" = ")
            value = int(value_s)
            pos = int(mem[4:-1])

            value = apply_mask2(value, mask)

            memory[pos] = value

    return memory


with open("day-14/example.txt") as f:
    program = f.readlines()
    memory = initialize(program)
    assert 165 == sum(memory.values())


with open("day-14/input.txt") as f:
    program = f.readlines()
    memory = initialize(program)
    print("Part 1: The sum of all values in memory is:", sum(memory.values()))
