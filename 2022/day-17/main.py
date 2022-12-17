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

def apply_direction(position: tuple, delta: tuple) -> tuple:
    return (position[0] + delta[0], position[1] + delta[1])

def move(rock: set, jet_direction: tuple) -> set:
    return {apply_direction(x, jet_direction) for x in rock}

def hits_wall(rock: set) -> bool:
    return (min(rock, key=lambda x: x[0])[0] < 0) or (max(rock, key=lambda x: x[0])[0] >= 7)

def hits_floor(rock: set) -> bool:
    return min(rock, key=lambda x: x[1])[1] < 0

def make_rocks_fall(jets: List[tuple], rock_amount: int) -> int:
    grid = set()
    rock_type = 0
    highest = -1

    fallen_rocks = 0
    i = 0

    cycles_height = 0
    seen_states = {}

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

        if not cycles_height:
            top_rows = {(x, highest - y) for (x, y) in grid if highest - y < 40}
            entry_key = (rock_type, i, frozenset(top_rows))
            if entry_key in seen_states:
                starting_highest, starting_fallen_rocks = seen_states[entry_key]
                cycle_length = fallen_rocks - starting_fallen_rocks
                cycle_size = highest - starting_highest

                num_cycles = (rock_amount - fallen_rocks) // cycle_length
                fallen_rocks = fallen_rocks + (cycle_length * num_cycles)
                cycles_height = num_cycles * cycle_size
            else:
                seen_states[entry_key] = (highest, fallen_rocks)

    return highest + 1 + cycles_height

with open("2022/day-17/example.txt", encoding="utf-8") as f:
    jets = [jet[j] for j in f.read().strip()]

    assert 1 == make_rocks_fall(jets, 1)
    assert 4 == make_rocks_fall(jets, 2)
    assert 6 == make_rocks_fall(jets, 3)
    assert 3068 == make_rocks_fall(jets, 2022)
    assert 1514285714288 == make_rocks_fall(jets, 1000000000000)

with open("2022/day-17/input.txt", encoding="utf-8") as f:
    jets = [jet[j] for j in f.read().strip()]

    print("Part 1: Tower height with 2022 rocks is:", make_rocks_fall(jets, 2022))
    print("Part 2: Tower height with 1 trillion rocks is:", make_rocks_fall(jets, 1000000000000))
