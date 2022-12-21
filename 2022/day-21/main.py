from typing import List

def parse_input(lines: List) -> dict:
    monkeys = {}
    for line in lines:
        parts = line.replace(':', '').split(' ')
        if len(parts) == 2:
            monkeys[parts[0]] = (int(parts[1]),)
        else:
            monkeys[parts[0]] = (parts[1], parts[2], parts[3])
    return monkeys

def hear_monkeys(monkeys: dict, leader: str) -> int:
    shouts = {}
    leader_found = False

    while not leader_found:
        for monkey_name, monkey_value in monkeys.items():
            if len(monkey_value) == 1:
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
    
    return shouts[leader]


with open("2022/day-21/example.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines()]
    monkeys = parse_input(lines)

    assert 152 == hear_monkeys(monkeys, 'root')

with open("2022/day-21/input.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines()]
    monkeys = parse_input(lines)

    print("Part 1: The number of root is:", hear_monkeys(monkeys, 'root'))