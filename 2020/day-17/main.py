from typing import List


def parse_input(notes: List[str]):
    lines = []
    for line in notes:
        lines.append(list(line.rstrip()))

    return lines


def read_initial_set(initial_state: List[str], dimensions: int) -> set:

    active_set = set()

    for y in range(len(initial_state)):
        for x in range(len(initial_state[0])):
            if initial_state[y][x] == '#':
                if dimensions == 3:
                    active_set.add((0, y, x))
                else:
                    active_set.add((0, 0, y, x))

    return active_set


def apply_cicles(initial_state: List[str], repeats: int) -> int:
    active = read_initial_set(initial_state, 3)

    for _ in range(repeats):
        minval = min(min(val for val in act) for act in active)
        maxval = max(max(val for val in act) for act in active)

        new_actives = set()

        for z in range(minval-1, maxval+2):
            for y in range(minval-1, maxval+2):
                for x in range(minval-1, maxval+2):
                    actcount = 0

                    for zdiff in range(-1, 2):
                        for ydiff in range(-1, 2):
                            for xdiff in range(-1, 2):
                                if zdiff == 0 and ydiff == 0 and xdiff == 0:
                                    continue

                                if (z+zdiff, y+ydiff, x+xdiff) in active:
                                    actcount += 1

                    if actcount == 3 or (actcount == 2 and (z, y, x)
                                         in active):
                        new_actives.add((z, y, x))

        active = new_actives

    return len(active)


def apply_cicles_4D(initial_state: List[str], repeats: int) -> int:
    active = read_initial_set(initial_state, 4)

    for _ in range(repeats):
        minval = min(min(val for val in act) for act in active)
        maxval = max(max(val for val in act) for act in active)

        new_actives = set()

        for w in range(minval-1, maxval+2):
            for z in range(minval-1, maxval+2):
                for y in range(minval-1, maxval+2):
                    for x in range(minval-1, maxval+2):
                        actcount = 0

                        for wdiff in range(-1, 2):
                            for zdiff in range(-1, 2):
                                for ydiff in range(-1, 2):
                                    for xdiff in range(-1, 2):
                                        if wdiff == 0 and zdiff == 0 and ydiff == 0 and xdiff == 0:
                                            continue

                                        if (w+wdiff, z+zdiff, y+ydiff, x+xdiff) in active:
                                            actcount += 1

                        if actcount == 3 or (actcount == 2 and (w, z, y, x) in active):
                            new_actives.add((w, z, y, x))

        active = new_actives

    return len(active)


with open("2020/day-17/example.txt") as f:
    initial_state = parse_input(f.readlines())
    assert 112 == apply_cicles(initial_state, 6)
    assert 848 == apply_cicles_4D(initial_state, 6)


with open("2020/day-17/input.txt") as f:
    initial_state = parse_input(f.readlines())
    print("Part 1: The active cubes after 6 repeats are:",
          apply_cicles(initial_state, 6))
    print("Part 2: The active cubes after 6 repeats in 4D are:",
          apply_cicles_4D(initial_state, 6))
