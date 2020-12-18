from typing import List
from operator import add, mul
from collections import deque


def tokenize(expression: str):
    ops = {"+": add, "*": mul}
    for char in expression:
        if char.isdigit():
            yield int(char)
        elif char in ops:
            yield ops[char]
        elif char in "()":
            yield char


def evaluate_expression(tokens: str) -> int:
    memory = deque()

    for token in tokens:
        if token == "(":
            memory.append(evaluate_expression(tokens))
        elif token == ")":
            break
        else:
            memory.append(token)

        if len(memory) > 2:
            left, op, right = memory.popleft(), memory.popleft(), memory.popleft()
            memory.append(op(left, right))

    return memory.popleft()


def calculate_by_precedence(lines: List[str], precendence: str) -> List[int]:
    results = []

    for line in lines:
        if precendence == 'left':
            res = evaluate_expression(tokenize(line))
        results.append(res)

    return results


with open("day-18/example.txt") as f:
    results = calculate_by_precedence(f.readlines(), "left")
    assert 71 == results[0]
    assert 51 == results[1]
    assert 26 == results[2]
    assert 437 == results[3]
    assert 12240 == results[4]
    assert 13632 == results[5]


with open("day-18/input.txt") as f:
    results = calculate_by_precedence(f.readlines(), "left")
    print("Part 1: Sum of evaluated values is: ", sum(results))
