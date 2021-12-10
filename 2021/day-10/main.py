from typing import List
from operator import add, mul
from collections import deque


def calculate_completion_score(queue: deque) -> int:
    print(queue)
    return 1


def calculate_syntax_score(line: str) -> int:
    memory = deque()
    syntax_score = 0
    completion_score = 0

    for token in line:
        if token == "(" or token == "[" or token == "<" or token == "{":
            memory.append(token)
        elif token == ")":
            precedent = memory.pop()
            if precedent != "(":
                syntax_score = 3
        elif token == "]":
            precedent = memory.pop()
            if precedent != "[":
                syntax_score = 57
        elif token == "}":
            precedent = memory.pop()
            if precedent != "{":
                syntax_score = 1197
        elif token == ">":
            precedent = memory.pop()
            if precedent != "<":
                syntax_score = 25137
        else:
            print("INCOMPLETE ---->", memory)
            break

    if syntax_score == 0:
        completion_score = calculate_completion_score(memory)

    return syntax_score, completion_score


def calculate_total_syntax_score(lines: List[str]) -> (int, int):

    sum_syntax_score = 0
    completion_scores = []
    for line in lines:
        syntax_score, completion_score = calculate_syntax_score(line)
        sum_syntax_score += syntax_score
        completion_scores.append(completion_score)

    return sum_syntax_score, len(completion_scores)


with open("2021/day-10/example.txt") as f:
    input = [str(line.strip()) for line in f]
    syntax_score, completion_score = calculate_total_syntax_score(input)
    assert 26397 == syntax_score

with open("2021/day-10/input.txt") as f:
    input = [str(line.strip()) for line in f]
    syntax_score, completion_score = calculate_total_syntax_score(input)
    print("Part 1: Total syntax error score is: ", syntax_score)
#     results = calculate_by_precedence(input, "mixed")
#     print("Part 2: Sum by mixed preference evaluation is: ", sum(results))
