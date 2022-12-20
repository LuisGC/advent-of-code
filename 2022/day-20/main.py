from typing import List

class Node:
    def __init__(self, value: int, index: int):
        self.value = value
        self.index = index

def mix(numbers: List[Node], iterations: int = 1) -> List[Node]:
    copy = numbers.copy()

    for _ in range(iterations):
        for node in numbers:
            index = copy.index(node)
            copy.pop(index)
            j = (index + node.value) % len(copy)
            if j == 0:
                j = len(copy)
            copy.insert(j, node)

    return copy

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

    numbers_with_key = [Node(int(x) * 811589153, i) for i, x in enumerate(input_lines)]
    mixed = mix(numbers_with_key, 10)
    assert 1623178306 == coords_sum(mixed)

with open("2022/day-20/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    numbers = [Node(int(x), i) for i, x in enumerate(input_lines)]
    mixed = mix(numbers)
    print("Part 1: Sum of indexes is:", coords_sum(mixed))

    numbers_with_key = [Node(int(x) * 811589153, i) for i, x in enumerate(input_lines)]
    mixed = mix(numbers_with_key, 10)
    print("Part 1: Sum of indexes is:", coords_sum(mixed))
