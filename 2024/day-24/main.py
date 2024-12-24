from typing import Tuple, List

def parse_input(input_file: str) -> Tuple[dict, dict]:
    content = [s.strip().split("\n") for s in input_file.rstrip().split("\n\n")]
    states = {n: g == "1" for n, g in map(lambda l: l.split(": "), content[0])}
    gates = {r1: (o1, o2, o3) for o1, o2, o3, _, r1 in map(lambda l: l.split(" "), content[1])}
    return states, gates

def get_state(key: str, states: dict, gates: dict) -> bool:
    if key in states:
        return states[key]
    i1, operator, i2 = gates[key]
    v1, v2 = get_state(i1, states, gates), get_state(i2, states, gates)
    match operator:
        case "AND":
            states[key] = v1 and v2
        case "OR": 
            states[key] = v1 or v2
        case 'XOR':
            states[key] = (v1 != v2)
        case _:
            raise ValueError(f"Unknown operator {operator}")
    return states[key]


def decimal_output(states: dict, gates: dict) -> int:
    num = ''
    key = 0
    while True:
        s_key = f'z{key:02d}'
        if s_key in states:
            num = str(int(states[s_key])) + num
            key += 1
        elif s_key in gates:
            num = str(int(get_state(s_key, states, gates))) + num
            key += 1
        else:
            break
    return int(num, 2)


with open("2024/day-24/example.txt", encoding="utf-8") as f:
    states, gates = parse_input(f.read())
    
    assert 4 == decimal_output(states, gates)

with open("2024/day-24/larger-example.txt", encoding="utf-8") as f:
    states, gates = parse_input(f.read())
    
    assert 2024 == decimal_output(states, gates)

with open("2024/day-24/input.txt", encoding="utf-8") as f:
    states, gates = parse_input(f.read())

    print(f"Part 1: Sum of possible designs is {decimal_output(states, gates)}")