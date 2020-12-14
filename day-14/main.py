from typing import Dict, List, Iterator
from collections import defaultdict
import itertools


def to_binary(value: int, num_digits: int = 36) -> List[int]:
    digits = []
    for _ in range(num_digits):
        digits.append(value % 2)
        value = value // 2
    return list(reversed(digits))


def parse_instruction(instruction: str):
    mem, value_s = instruction.split(" = ")
    value = int(value_s)
    address = int(mem[4:-1])
    return address, value


def initialize_decoder(instructions: List[str]) -> Dict[int, int]:
    memory = defaultdict(int)
    mask = None

    for line in instructions:
        if line.startswith("mask"):
            mask = line.split()[-1]
        else:
            address, value = parse_instruction(line)

            for pos in apply_multi_mask(address, mask):
                memory[pos] = value

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
                pass  # leave unchanged
            elif m == '1':
                new_digits[i] = 1  # overwrite with 1
            else:
                new_digits[i] = next(it)  # wildcard iteration

        yield sum(digit * (2 ** i)
                  for i, digit in enumerate(reversed(new_digits)))


def initialize_memory(instructions):
    memory = defaultdict(int)
    mask = None

    for line in instructions:
        if line.startswith("mask"):
            mask = line.split()[-1]
            continue

        address, value = parse_instruction(line)

        binary_value = bin(value)[2:]
        binary_value = '0' * (len(mask) - len(binary_value)) + binary_value
        bin_len = len(binary_value)
        final = []

        for bin_pos in range(-1, -bin_len-1, -1):
            if mask[bin_pos] == 'X':
                final.append(binary_value[bin_pos])
            else:
                final.append(mask[bin_pos])

        rev = ''.join(list(final)[::-1])

        memory[address] = int(rev, 2)

    return memory


with open("day-14/example.txt") as f:
    program = f.readlines()
    memory = initialize_memory(program)
    assert 165 == sum(memory.values())


with open("day-14/decoder-example.txt") as f:
    program = f.readlines()
    memory = initialize_decoder(program)
    assert 208 == sum(memory.values())


with open("day-14/input.txt") as f:
    program = f.readlines()
    memory = initialize_memory(program)
    print("Part 1: The sum of all values in memory is:",
          sum(memory.values()))
    memory = initialize_decoder(program)
    print("Part 2: The sum of all values in memory with decoder is:",
          sum(memory.values()))
