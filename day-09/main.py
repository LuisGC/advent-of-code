from typing import List
from collections import deque

def find_encoding_errors (numbers: List[int], lookback: int = 25) -> List[int]:
    q = deque()
    result = []

    for n in numbers:
        if len(q) < lookback:
            q.append(n)
        else:
            sums = {a + b
                    for i, a in enumerate(q)
                    for j, b in enumerate(q)
                    if i < j}
            if n not in sums:
                result.append(n)
            q.append(n)
            q.popleft()

    return result

with open("day-09/example.txt") as f:
    raw = f.read().strip()
    numbers = [int(x) for x in raw.split("\n")]
    assert 127 == find_encoding_errors(numbers,5)[0]

with open("day-09/input.txt") as f:
    raw = f.read().strip()
    numbers = [int(x) for x in raw.split("\n")]
    print("Part 1: The first encoding error is", find_encoding_errors(numbers,25)[0])
