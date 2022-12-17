from typing import List

DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

jet = {"<": LEFT, ">": RIGHT}

def make_rock(type: int, pos: tuple) -> set:
    rock = []
    x, y = pos

    if type == 0:
        rock = [(x + i, y) for i in range(4)]
    elif type == 1:
        rock = [(x + i, y + 1) for i in range(3)]
        rock += [(x + 1, y + i) for i in range(3)]
    elif type == 2:
        rock = [(x + i, y) for i in range(3)]
        rock += [(x + 2, y + i) for i in range(3)]
    elif type == 3:
        rock = [(x, y + i) for i in range(4)]
    elif type == 4:
        rock = [(x + i, y + j) for i in range(2) for j in range(2)]

    return set(rock)

def add_pair(a: tuple, b: tuple) -> tuple:
    return (a[0] + b[0], a[1] + b[1])

def move(rock: set, dir: tuple) -> set:
    return {add_pair(x, dir) for x in rock}

def hits_wall(rock: set) -> bool:
    return (min(rock, key=lambda x: x[0])[0] < 0) or (max(rock, key=lambda x: x[0])[0] >= 7)

def hits_floor(rock: set) -> bool:
    return min(rock, key=lambda x: x[1])[1] < 0

def make_rocks_fall(jets: List[tuple], rock_amount: int = 2022) -> int:
    grid = set()
    rock_type = 0
    highest = -1

    fallen_rocks = 0
    i = 0
    while fallen_rocks < rock_amount:
        rock = make_rock(rock_type, (2, highest + 4))

        while(True):
            jet = jets[i]
            i = (i + 1) % len(jets)
            next = move(rock, jet)

            if not hits_wall(next) and not next.intersection(grid):
                rock = next

            next = move(rock, DOWN)
            if not hits_floor(next) and not next.intersection(grid):
                rock = next
            else:
                grid = grid.union(rock)
                highest = max(grid, key=lambda x: x[1])[1]
                fallen_rocks += 1
                rock_type = (rock_type + 1) % 5
                break

    return highest + 1

with open("2022/day-17/example.txt", encoding="utf-8") as f:
    jets = [jet[j] for j in f.read().strip()]

    assert 1 == make_rocks_fall(jets, 1)
    assert 4 == make_rocks_fall(jets, 2)
    assert 6 == make_rocks_fall(jets, 3)
    assert 3068 == make_rocks_fall(jets)
#    assert 1514285714288 == make_rocks_fall(jets, 1000000000000)

with open("2022/day-17/input.txt", encoding="utf-8") as f:
    jets = [jet[j] for j in f.read().strip()]

    print("Part 1: Tower height is:", make_rocks_fall(jets))
#    print("Part 2: Tower height is:", make_rocks_fall(jets, 1000000000000))
