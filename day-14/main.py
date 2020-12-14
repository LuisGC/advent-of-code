from typing import Dict, List, Iterator
from collections import defaultdict
import itertools


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


def initialize(program: List[str], mode: str) -> Dict[int, int]:
    memory = defaultdict(int)
    mask = None

    for line in program:
        if line.startswith("mask"):
            mask = line.split(" = ")[-1]
        else:
            mem, value_s = line.split(" = ")
            value = int(value_s)
            pos = int(mem[4:-1])

            if mode == 'mask':
                value = apply_mask2(value, mask)
                memory[pos] = value
            else:
                for pos2 in apply_multi_mask(pos, mask):
                    memory[pos2] = value

    return memory


def apply_multi_mask(value: int, mask: str) -> Iterator[int]:
    digits = to_binary(value)

    xs = [i for i, c in enumerate(mask) if c == 'X']
    sub_values = [[0, 1] for _ in xs]
    for choice in itertools.product(*sub_values):
        new_digits = digits[:]
        it = iter(choice)
        for i, (digit, m) in enumerate(zip(digits, mask)):
            if m == '0':
                pass  # leave the digit as is
            elif m == '1':
                new_digits[i] = 1
            else:
                new_digits[i] = next(it)

        yield sum(digit * (2 ** i) for i, digit in enumerate(reversed(new_digits)))


with open("day-14/example.txt") as f:
    program = f.readlines()
    memory = initialize(program, 'mask')
    assert 165 == sum(memory.values())


with open("day-14/decoder-example.txt") as f:
    program = f.readlines()
    memory = initialize(program, 'decoder')
    assert 208 == sum(memory.values())


with open("day-14/input.txt") as f:
    program = f.readlines()
    memory = initialize(program, 'mask')
    print("Part 1: The sum of all values in memory is:",
          sum(memory.values()))
    memory = initialize(program, 'decoder')
    print("Part 2: The sum of all values in memory with version 2 is:",
          sum(memory.values()))
