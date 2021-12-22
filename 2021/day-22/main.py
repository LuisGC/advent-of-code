from typing import List

class Range():
    def __init__(self, pair: List[str]):
        self.min = int(pair[0])
        self.max = int(pair[1])

def parse_input(input: List[str]) -> List:
    steps = []
    for line in input:
        status, coords = line.split(" ")
        cuboid = [x.split('=')[1].split('..') for x in coords.split(',')]
        steps += [(status == "on", Range(cuboid[0]), Range(cuboid[1]), Range(cuboid[2]))]
    return steps


def setGrid(steps: List, region_limit: int) -> set:
    grid = set()
    for st, rangex, rangey, rangez in steps:
        for x in range(max(rangex.min, -region_limit), min(rangex.max, region_limit)+1):
            for y in range(max(rangey.min, -region_limit), min(rangey.max, region_limit)+1):
                for z in range(max(rangez.min, -region_limit), min(rangez.max, region_limit)+1):
                    if st:
                        grid.add((x, y, z))
                    elif (x, y, z) in grid:
                        grid.remove((x, y, z))
    return grid

with open("2021/day-22/example.txt") as f:
    steps = parse_input([str(line.strip()) for line in f])
    grid = setGrid(steps, 50)
    assert 39 == len(grid)

with open("2021/day-22/larger-example.txt") as f:
    steps = parse_input([str(line.strip()) for line in f])
    grid = setGrid(steps, 50)
    assert 590784 == len(grid)

with open("2021/day-22/largest-example.txt") as f:
    steps = parse_input([str(line.strip()) for line in f])
    grid = setGrid(steps, 50)
    assert 474140 == len(grid)
    # grid = setGrid(steps, 150000)
    # assert 2758514936282235 == len(grid)

with open("2021/day-22/input.txt") as f:
    steps = parse_input([str(line.strip()) for line in f])
    grid = setGrid(steps, 50)
    print("Part 1: The amount of cubes is:", len(grid))
#     print("Part 2: The wins of the player that wins most is:", max(quantum_game.wins))
