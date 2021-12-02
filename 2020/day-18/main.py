from typing import List
from operator import add, mul
from collections import deque


def tokenize(expression: str):
    for char in expression:
        if char.isdigit():
            yield int(char)
        elif char == "+":
            yield add
        elif char == "*":
            yield mul
        elif char in "()":
            yield char


def evaluate_left_precedence(tokens: str) -> int:
    memory = deque()

    for token in tokens:
        if token == "(":
            memory.append(evaluate_left_precedence(tokens))
        elif token == ")":
            break
        else:
            memory.append(token)

        if len(memory) > 2:
            left, op, right = memory.popleft(), memory.popleft(), memory.popleft()
            memory.append(op(left, right))

    return memory.popleft()


def evaluate_mixed_precedence(tokens: str) -> int:
    memory = deque()

    for token in tokens:
        if token == "(":
            memory.append(evaluate_mixed_precedence(tokens))
        elif token == ")":
            break
        else:
            memory.append(token)

        if len(memory) > 2:
            if memory[-2] == add:
                right, op, left = memory.pop(), memory.pop(), memory.pop()
                memory.append(op(left, right))

    while len(memory) > 1:
        left, op, right = memory.popleft(), memory.popleft(), memory.popleft()
        memory.appendleft(op(left, right))

    return memory.popleft()


def calculate_by_precedence(lines: List[str], precendence: str) -> List[int]:

    results = []
    for line in lines:
        if precendence == 'left':
            res = evaluate_left_precedence(tokenize(line))
        else:
            res = evaluate_mixed_precedence(tokenize(line))
        results.append(res)

    return results


with open("2020/day-18/example.txt") as f:
    input = f.readlines()
    results = calculate_by_precedence(input, "left")
    assert 71 == results[0]
    assert 51 == results[1]
    assert 26 == results[2]
    assert 437 == results[3]
    assert 12240 == results[4]
    assert 13632 == results[5]
    results = calculate_by_precedence(input, "mixed")
    assert 231 == results[0]
    assert 51 == results[1]
    assert 46 == results[2]
    assert 1445 == results[3]
    assert 669060 == results[4]
    assert 23340 == results[5]


with open("2020/day-18/input.txt") as f:
    input = f.readlines()
    results = calculate_by_precedence(input, "left")
    print("Part 1: Sum by left preference evaluation is: ", sum(results))
    results = calculate_by_precedence(input, "mixed")
    print("Part 2: Sum by mixed preference evaluation is: ", sum(results))
