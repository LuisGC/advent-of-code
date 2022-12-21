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

def guess_my_number(monkeys: dict, leader: str='root', my_name: str='humn') -> int:
    shouts = {}
    leader_found = False
    my_number = 0 # >63510129 for test and did not finish

    while not leader_found:
        for monkey_name, monkey_value in monkeys.items():
            if monkey_name == leader:
                if monkey_value[0] in shouts and monkey_value[2] in shouts:
                    if monkey_value[0] == monkey_value[2]:
                        leader_found = True
                        break
                    else:
                        shouts = {}
                        my_number += 1
            elif monkey_name == my_name:
                shouts[monkey_name] = my_number
            elif len(monkey_value) == 1:
                shouts[monkey_name] = monkey_value[0]
            else:
                if monkey_value[0] in shouts and monkey_value[2] in shouts:
                    if monkey_value[1] == '+':
                        shouts[monkey_name] = shouts[monkey_value[0]] + shouts[monkey_value[2]]
                    elif monkey_value[1] == '-':
                        shouts[monkey_name] = shouts[monkey_value[0]] - shouts[monkey_value[2]]
                    elif monkey_value[1] == '*':
                        shouts[monkey_name] = shouts[monkey_value[0]] * shouts[monkey_value[2]]
                    elif monkey_value[1] == '/':
                        shouts[monkey_name] = shouts[monkey_value[0]] // shouts[monkey_value[2]]
                    else:
                        raise ValueError("Invalid operation")

                    if monkey_name == leader:
                        leader_found = True
                        break
    
    return my_number


with open("2022/day-21/example.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines()]
    monkeys = parse_input(lines)

    assert 152 == hear_monkeys(monkeys)
    # assert 31 == guess_my_number(monkeys)

with open("2022/day-21/input.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines()]
    monkeys = parse_input(lines)

    print("Part 1: The number of root is:", hear_monkeys(monkeys))
    # print("Part 2: The number of humn must be:", guess_my_number(monkeys))