from typing import List

class Range():
    def __init__(self, pair: List[str]):
        self.min = int(pair[0])
        self.max = int(pair[1])

    def __str__(self):
        return "<" + str(self.min) + ".." + str(self.max) + ">"


class Cuboid():
    def __init__(self, status: str, rangex: List, rangey: List, rangez: List):
        self.status = status == "on"
        self.rangex = Range(rangex)
        self.rangey = Range(rangey)
        self.rangez = Range(rangez)

    def __str__(self):
        string = "Status: " + str(self.status)
        string += " X=" + str(self.rangex)
        string += " Y=" + str(self.rangey)
        string += " Z=" + str(self.rangez)
        return(string)


def parse_input(input: List[str]) -> List:
    cuboids = []
    for line in input:
        status, coords = line.split(" ")
        cuboid = [x.split('=')[1].split('..') for x in coords.split(',')]
        cuboids.append(Cuboid(status, cuboid[0], cuboid[1], cuboid[2]))

    return cuboids


def setGrid(cuboids: List[Cuboid], region_limit: int) -> set:
    grid = set()
    for cuboid in cuboids:
        for x in range(max(cuboid.rangex.min, -region_limit), min(cuboid.rangex.max, region_limit)+1):
            for y in range(max(cuboid.rangey.min, -region_limit), min(cuboid.rangey.max, region_limit)+1):
                for z in range(max(cuboid.rangez.min, -region_limit), min(cuboid.rangez.max, region_limit)+1):
                    if cuboid.status:
                        grid.add((x, y, z))
                    elif (x, y, z) in grid:
                        grid.remove((x, y, z))
    return grid

with open("2021/day-22/example.txt") as f:
    cuboids = parse_input([str(line.strip()) for line in f])
    grid = setGrid(cuboids, 50)
    assert 39 == len(grid)

with open("2021/day-22/larger-example.txt") as f:
    cuboids = parse_input([str(line.strip()) for line in f])
    grid = setGrid(cuboids, 50)
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
