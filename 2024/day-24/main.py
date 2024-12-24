from itertools import combinations
from typing import Tuple, Optional
import sys
sys.path.insert(0, './')
from utils import profiler

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

@profiler
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

def furthest_made(gates: dict, max_z: int) -> Tuple[int, set]:
    ops = {}
    for res, (x1, op, x2) in gates.items():
        ops[(frozenset([x1, x2]), op)] = res

    def get_res(x1_, x2_, op_) -> Optional[int]:
        return ops.get((frozenset([x1_, x2_]), op_), None)

    carries = {}
    correct = set()
    prev_intermediaries = set()
    for i in range(max_z):
        prev_digit = get_res(f"x{i:02d}", f"y{i:02d}", "XOR")
        prev_carry1 = get_res(f"x{i:02d}", f"y{i:02d}", "AND")
        if i == 0:
            carries[i] = prev_carry1
            continue
        digit = get_res(carries[i - 1], prev_digit, "XOR")
        if digit != f"z{i:02d}":
            return i - 1, correct
        correct.add(carries[i - 1])
        correct.add(prev_digit)
        for wire in prev_intermediaries:
            correct.add(wire)
        
        prev_carry2 = get_res(carries[i - 1], prev_digit, "AND")
        carry_out = get_res(prev_carry1, prev_carry2, "OR")
        carries[i] = carry_out

        prev_intermediaries = {prev_carry1, prev_carry2}

    return max_z, correct
    
@profiler
def swapping_gates(gates: dict, max_z: int = 45) -> int:
    swaps = set()
    base, used = furthest_made(gates, max_z)

    for _ in range(4):
        for res_i, res_j in combinations(gates.keys(), 2):
            if "z00" in (res_i, res_j) or res_i in used or res_j in used:
                continue
            gates[res_i], gates[res_j] = gates[res_j], gates[res_i]
            attempt, attempt_used = furthest_made(gates, max_z)
            if attempt > base:
                swaps.add((res_i, res_j))
                base, used = attempt, attempt_used
                break
            gates[res_i], gates[res_j] = gates[res_j], gates[res_i]

    return ",".join(sorted(sum(swaps, start=tuple())))


with open("2024/day-24/example.txt", encoding="utf-8") as f:
    states, gates = parse_input(f.read())
    
    assert 4 == decimal_output(states, gates)

with open("2024/day-24/larger-example.txt", encoding="utf-8") as f:
    states, gates = parse_input(f.read())
    
    assert 2024 == decimal_output(states, gates)

with open("2024/day-24/example-2.txt", encoding="utf-8") as f:
    states, gates = parse_input(f.read())
    
    assert 9 == decimal_output(states, gates)

with open("2024/day-24/input.txt", encoding="utf-8") as f:
    states, gates = parse_input(f.read())

    print(f"Part 1: Sum of possible designs is {decimal_output(states, gates)}")
    print(f"Part 2: Swapping gates and sorting result: {swapping_gates(gates, max_z=45)}")