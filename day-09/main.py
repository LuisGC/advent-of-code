from typing import List
from collections import deque

def first_encoding_error (numbers: List[int], lookback) -> int:
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

def find_encryption_weakness(numbers: List[int], encoding_error: int) -> int:

    range = []

    for i, n in enumerate(numbers):
        j = i
        total = n
        while total < encoding_error and j < len(numbers):
            j += 1
            total += numbers[j]
        if total == encoding_error and i < j:
            range = numbers[i:j+1]

    if len(range) == 0:
        raise RuntimeError()

    return min(range) + max(range)

with open("day-09/example.txt") as f:
    raw = f.read().strip()
    numbers = [int(x) for x in raw.split("\n")]
    encoding_error = first_encoding_error(numbers,5)
    assert 127 == encoding_error
    assert 62 == find_encryption_weakness(numbers, encoding_error)

with open("day-09/input.txt") as f:
    raw = f.read().strip()
    numbers = [int(x) for x in raw.split("\n")]
    encoding_error = first_encoding_error(numbers,25)
    print("Part 1: The first encoding error is", encoding_error)
    print("Part 2: The encryption weakness is", find_encryption_weakness(numbers,encoding_error))
