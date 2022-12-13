from dataclasses import dataclass
from collections import deque
from typing import List

@dataclass
class Operation:
    left: int
    operand: str
    right: int

    def execute(self, old):
        if self.left == "old":
            left = old
        else:
            left = self.left
        if self.right == "old":
            right = old
        else:
            right = self.right

        if self.operand == "+":
            return left + right
        elif self.operand == "*":
            return left * right
        else:
            raise ValueError("Invalid operation")

@dataclass
class Monkey: 
    items: deque
    operation: Operation
    test: int
    true_next: int
    false_next: int
    inspections: int

    def set_operation(self, new_operation: Operation):
        self.operation.left = new_operation.left
        self.operation.operand = new_operation.operand
        self.operation.right = new_operation.right

def parse_input(lines: List) -> List[Monkey]:
    monkeys = []

    for line in lines:
        if line == "\n":
            continue
        parts = line.split(": ")
        # monkey = None
        if "Monkey" in parts[0]:
            monkey = Monkey(deque(), Operation(-1, "", -1), -1, -1, -1, 0)
            monkeys.append(monkey)
        elif "Starting" in parts[0]:
            items = parts[1].split(", ")
            for item in items:
                monkeys[-1].items.append(int(item))
        elif "Operation" in parts[0]:
            op_parts = parts[1].split(" ")
            left, right = "old", "old"
            if op_parts[2] != "old":
                left = int(op_parts[2])
            if op_parts[4] != "old":
                right = int(op_parts[4])
            monkeys[-1].set_operation(Operation(left, op_parts[3], right))
        elif "Test" in parts[0]:
            test_parts = parts[1].split(" ")
            monkeys[-1].test = int(test_parts[2])
        elif "If true" in parts[0]:
            parts = parts[1].split(" ")
            monkeys[-1].true_next = int(parts[3])
        elif "If false" in parts[0]:
            parts = parts[1].split(" ")
            monkeys[-1].false_next = int(parts[3])

    # print(monkeys)
    return monkeys

def print_monkey_items(monkeys: List[Monkey]):
    for i in range (len(monkeys)):
        print(f"  Monkey ", i , "[", monkeys[i].inspections, "]: ", monkeys[i].items)

def observe_monkeys(monkeys: List[Monkey], rounds: int = 20, basic_divide: bool = True):

    lcd = monkeys[0].test
    for i in range (1, len(monkeys)):
        if lcd % monkeys[i].test != 0:
            lcd *= monkeys[i].test

    for round in range(rounds):
        for monkey in monkeys:
            num_items = len(monkey.items)
            for _ in range(num_items):
                worry_level = monkey.items.popleft()
                worry_level = monkey.operation.execute(worry_level)
                if basic_divide:
                    worry_level = int(worry_level / 3)
                else:
                    worry_level = worry_level % lcd

                if worry_level % monkey.test == 0:
                    monkeys[monkey.true_next].items.append(worry_level)
                else:
                    monkeys[monkey.false_next].items.append(worry_level)
                monkey.inspections += 1

    monkeys.sort(key=lambda monkey: monkey.inspections)
    return monkeys[-2].inspections * monkeys[-1].inspections

# REFACTOR IS NEEDED to avoid parsing the input each time

with open("2022/day-11/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    assert 10605 == observe_monkeys(parse_input(input_lines))
    assert 6*4 == observe_monkeys(parse_input(input_lines), 1, False)
    assert 103*99 == observe_monkeys(parse_input(input_lines), 20, False)
    assert 5204*5192 == observe_monkeys(parse_input(input_lines), 1000, False)
    assert 10419*10391 == observe_monkeys(parse_input(input_lines), 2000, False)
    assert 15638*15593 == observe_monkeys(parse_input(input_lines), 3000, False)
    assert 20858*20797 == observe_monkeys(parse_input(input_lines), 4000, False)
    assert 26075*26000 == observe_monkeys(parse_input(input_lines), 5000, False)
    assert 31294*31204 == observe_monkeys(parse_input(input_lines), 6000, False)
    assert 36508*36400 == observe_monkeys(parse_input(input_lines), 7000, False)
    assert 41728*41606 == observe_monkeys(parse_input(input_lines), 8000, False)
    assert 46945*46807 == observe_monkeys(parse_input(input_lines), 9000, False)
    assert 52166*52013 == observe_monkeys(parse_input(input_lines), 10000, False)

with open("2022/day-11/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print("Part 1: Monkey business level is:", observe_monkeys(parse_input(input_lines)))
    print("Part 2: Monkey business in 10K rounds is:", observe_monkeys(parse_input(input_lines), 10000, False))
