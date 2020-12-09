from typing import List
from collections import deque

def first_encoding_error (numbers: List[int], lookback: int = 25) -> int:
    q = deque()
    result = 0

    for n in numbers:
        if len(q) < lookback:
            q.append(n)
        else:
            sums = {a + b
                    for i, a in enumerate(q)
                    for j, b in enumerate(q)
                    if i < j}
            if n not in sums:
                result = n
                break
            q.append(n)
            q.popleft()

    return result

with open("day-09/example.txt") as f:
    raw = f.read().strip()
    numbers = [int(x) for x in raw.split("\n")]
    assert 127 == first_encoding_error(numbers,5)

with open("day-09/input.txt") as f:
    raw = f.read().strip()
    numbers = [int(x) for x in raw.split("\n")]
    print("Part 1: The first encoding error is", first_encoding_error(numbers,25))
