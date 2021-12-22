from typing import List

def parse_input(input: List[str]) -> List:
    steps = []
    for line in input:
        status, coords = line.split(" ")
        cuboid = [x.split('=')[1].split('..') for x in coords.split(',')]
        steps += [(status == "on", int(cuboid[0][0]), int(cuboid[0][1]), int(cuboid[1][0]), int(cuboid[1][1]), int(cuboid[2][0]), int(cuboid[2][1]))]
    return steps


def setGrid(steps: List) -> set:
    grid = set()
    for st, xmin, xmax, ymin, ymax, zmin, zmax in steps:
        for x in range(max(xmin, -50), min(xmax, 50)+1):
            for y in range(max(ymin, -50), min(ymax, 50)+1):
                for z in range(max(zmin, -50), min(zmax, 50)+1):
                    # if not (x >= -50 and x <= 50 and y >= -50 and y <= 50 and z >= -50 and z <= 50):
                    #     continue
                    # print(st, x, y, z)
                    if st:
                        grid.add((x, y, z))
                    elif (x, y, z) in grid:
                        grid.remove((x, y, z))
    return grid

with open("2021/day-22/example.txt") as f:
    steps = parse_input([str(line.strip()) for line in f])
    grid = setGrid(steps)
    assert 39 == len(grid)

with open("2021/day-22/larger-example.txt") as f:
    steps = parse_input([str(line.strip()) for line in f])
    grid = setGrid(steps)
    assert 590784 == len(grid)

with open("2021/day-22/largest-example.txt") as f:
    steps = parse_input([str(line.strip()) for line in f])
    grid = setGrid(steps)
    assert 474140 == len(grid)

with open("2021/day-22/input.txt") as f:
    steps = parse_input([str(line.strip()) for line in f])
    grid = setGrid(steps)
    print("Part 1: The amount of cubes is:", len(grid))
#     print("Part 2: The wins of the player that wins most is:", max(quantum_game.wins))
