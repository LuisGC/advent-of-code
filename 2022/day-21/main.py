from typing import List
import re
import operator

def parse_input(lines: List) -> dict:
    MONKEY_WITH_VALUE = re.compile(r'(\w{4}): (\d+)')
    MONKEY_WITH_OP = re.compile(r'(\w{4}): (\w{4}) ([-+*/]) (\w{4})')
    OPERATIONS = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv}

    monkeys = {}
    for line in lines:
        if monkey := MONKEY_WITH_VALUE.match(line):
            name, value = monkey.groups()
            monkeys[name] = (int(value),)
        elif monkey := MONKEY_WITH_OP.match(line):
            name, arg_left, op, arg_right = monkey.groups()
            monkeys[name] = (arg_left, arg_right, OPERATIONS[op], op)
        else:
            raise ValueError("Invalid monkey")
    return monkeys

def resolve(monkeys: dict, name: str) -> int:
    value = monkeys[name]
    if len(value) == 1:
        return value[0]
    left = resolve(monkeys, value[0])
    right = resolve(monkeys, value[1])
    return value[2](left, right)

def hear_monkeys(monkeys: dict, leader: str='root') -> int:
    return resolve(monkeys, leader)

def dependencies(monkeys: dict, name: str):
    value = monkeys[name]
    if len(value) == 1:
        return set((name,))
    left = dependencies(monkeys, value[0])
    right = dependencies(monkeys, value[1])
    return left | right

def guess_my_number(monkeys: dict, leader: str='root', my_name: str='humn') -> int:
    my_number = 0
    left = dependencies(monkeys, monkeys[leader][0])
    right = dependencies(monkeys, monkeys[leader][1])

    root = leader
    if my_name in left and my_name in right:
        raise ValueError("Unexpected error")
    elif my_name in left:
        my_number = resolve(monkeys, monkeys[leader][1])
        root = monkeys[leader][0]
    else:
        my_number = resolve(monkeys, monkeys[leader][0])
        root = monkeys[leader][1]

    while root != my_name:
        left = dependencies(monkeys, monkeys[root][0])
        right = dependencies(monkeys, monkeys[root][1])
        if my_name in left and my_name in right:
            raise ValueError("Unexpected error")

        # reverse the expression to solve for the variable
        if my_name in left:  # solve for left operand
            if monkeys[root][3] == '+':
                my_number -= resolve(monkeys, monkeys[root][1])
            elif monkeys[root][3] == '-':
                my_number += resolve(monkeys, monkeys[root][1])
            elif monkeys[root][3] == '*':
                my_number //= resolve(monkeys, monkeys[root][1])
            elif monkeys[root][3] == '/':
                my_number *= resolve(monkeys, monkeys[root][1])
            root = monkeys[root][0]
        else:  # solve for right operand
            if monkeys[root][3] == '+':
                my_number -= resolve(monkeys, monkeys[root][0])
            elif monkeys[root][3] == '-':
                my_number = resolve(monkeys, monkeys[root][0]) - my_number
            elif monkeys[root][3] == '*':
                my_number //= resolve(monkeys, monkeys[root][0])
            elif monkeys[root][3] == '/':
                my_number = resolve(monkeys, monkeys[root][0]) // my_number
            root = monkeys[root][1]
    
    return my_number


with open("2022/day-21/example.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines()]
    monkeys = parse_input(lines)

    assert 152 == hear_monkeys(monkeys)
    assert 301 == guess_my_number(monkeys)

with open("2022/day-21/input.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines()]
    monkeys = parse_input(lines)

    print("Part 1: The number of root is:", hear_monkeys(monkeys))
    print("Part 2: The number of humn must be:", guess_my_number(monkeys))