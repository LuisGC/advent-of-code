from itertools import combinations
from math import dist

def connect_circuits(boxes: list[tuple[int]], iterations: int) -> tuple[int, int]:
    circuits = []
    prod_three_largest = prod_last_cable = 1

    distances = [(*pair, dist(*pair)) for pair in combinations(boxes, 2)]

    for i, (p, q, _) in enumerate(sorted(distances, key=lambda x: x[2])):
        s = {p, q}

        for circuit in circuits:
            if p not in circuit and q not in circuit:
                continue

            temp = [c for c in circuits if p not in c and q not in c]
            for box in filter(lambda c: p in c or q in c, circuits):
                s |= box
            temp.append(s)
            circuits = temp
            break
        else:
            circuits.append(set([p, q]))

        if i == iterations -1:
            lengths = sorted([len(circuit) for circuit in circuits], reverse=True)[:3]
            prod_three_largest = lengths[0] * lengths[1] * lengths[2]

        if len(circuits) == 1 and len(circuits[0]) == len(boxes):
            prod_last_cable = p[0] * q[0]
            break

    return prod_three_largest, prod_last_cable

with open("2025/day-08/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    boxes = [tuple(int(pos) for pos in line.split(",")) for line in input_lines]

    prod_three_largest, prod_last_cable = connect_circuits(boxes, 10)

    assert 40 == prod_three_largest
    assert 25272 == prod_last_cable

with open("2025/day-08/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    boxes = [tuple(int(pos) for pos in line.split(",")) for line in input_lines]

    prod_three_largest, prod_last_cable = connect_circuits(boxes, 1000)

    print(f"Part 1: The prod of the sizes of the three largest circuits is {prod_three_largest}")
    print(f"Part 2: The prod of x coordinates of the last cable is {prod_last_cable}")
