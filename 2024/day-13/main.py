from typing import List
import re

def fewest_tokens(blocks: List[str]) -> int:
    res = 0

    for block in blocks:
        ax, ay, bx, by, px, py = map(int, re.findall(r"\d+", block))
        score = float("inf")
        for i in range(101):
            for j in range(101):
                if ax * i + bx * j == px and ay*i + by * j == py:
                    score = min(score, 3*i + 1*j)
        if score != float("inf"):
            res += score
    return res


with open("2024/day-13/example.txt", encoding="utf-8") as f:
    input = f.read().rstrip().split("\n\n")
    assert 480 == fewest_tokens(input)

with open("2024/day-13/input.txt", encoding="utf-8") as f:
    input = f.read().rstrip().split("\n\n")
    print(f"Part 1: Fewest tokens is {fewest_tokens(input)}")
#    print(f"Part 2: Disk checksum without fragmentation is {disk.checksum()}")
