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

    def get_inspections(self):
        return self.inspections

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

def observe_monkeys(monkeys: List[Monkey], rounds: int = 20):

    for _ in range(rounds):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                item = monkey.items.popleft()
                worry_level = monkey.operation.execute(item)
                worry_level = int(worry_level / 3)
                if worry_level % monkey.test == 0:
                    monkeys[monkey.true_next].items.append(worry_level)
                else:
                    monkeys[monkey.false_next].items.append(worry_level)
                monkey.inspections += 1

    # print(monkeys)
    monkeys.sort(key=lambda monkey: monkey.inspections, reverse=True)
    return monkeys[0].inspections * monkeys[1].inspections

with open("2022/day-11/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    monkey_operations = parse_input(input_lines)

    assert 10605 == observe_monkeys(monkey_operations)

with open("2022/day-11/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    monkey_operations = parse_input(input_lines)

    print("Part 1: Monkey business level is:", observe_monkeys(monkey_operations))
#     print("Part 2: Count of visited positions by 9th knot are:", count_tail_visited_positions(head_movements, 9))
