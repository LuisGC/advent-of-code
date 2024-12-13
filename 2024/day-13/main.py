from typing import List
import re

def fewest_tokens(blocks: List[str], error: int = 0) -> int:
    res = 0

    for block in blocks:
        ax, ay, bx, by, px, py = map(int, re.findall(r"\d+", block))
        if error == 0:
            score = float("inf")
            for i in range(101):
                for j in range(101):
                    if ax * i + bx * j == px and ay*i + by * j == py:
                        score = min(score, 3*i + 1*j)
            if score != float("inf"):
                res += score
        else:
            px += error
            py += error
            ca = (px * by - py * bx) / (ax * by - ay * bx)
            cb = (px - ax * ca) / bx
            if ca % 1 == cb % 1 == 0:
                res += 3 * int(ca) + 1 * int(cb)
    return res


with open("2024/day-13/example.txt", encoding="utf-8") as f:
    input = f.read().rstrip().split("\n\n")
    assert 480 == fewest_tokens(input)

with open("2024/day-13/input.txt", encoding="utf-8") as f:
    input = f.read().rstrip().split("\n\n")
    print(f"Part 1: Fewest tokens is {fewest_tokens(input)}")
    print(f"Part 2: Fewest tokens with initial error is {fewest_tokens(input, 10000000000000)}")
