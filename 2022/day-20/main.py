from typing import List

class Node:
    def __init__(self, value: int, index: int):
        self.value = value
        self.index = index

def mix(numbers: List[Node]) -> List[Node]:
    original = numbers.copy()

    for node in original:
        index = numbers.index(node)
        numbers.pop(index)
        j = (index + node.value) % len(numbers)
        if j == 0:
            j = len(numbers)
        numbers.insert(j, node)

    return numbers

def coords_sum(nodes: List[Node]) -> int:
    zero_index = None

    for i in range(len(nodes)):
        if nodes[i].value == 0:
            zero_index = i
            break

    assert zero_index != None
    res = 0
    for val in [1000, 2000, 3000]:
        j = (zero_index + val) % len(nodes)
        res += nodes[j].value

    return res

with open("2022/day-20/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    numbers = [Node(int(x), i) for i, x in enumerate(input_lines)]

    mixed = mix(numbers)
    assert 3 == coords_sum(mixed)

with open("2022/day-20/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    numbers = [Node(int(x), i) for i, x in enumerate(input_lines)]

    mixed = mix(numbers)
    
    print("Part 1: Sum of indexes is:", coords_sum(mixed))
