from typing import List

class Range():
    def __init__(self, minimum, maximum):
        self.minimum = int(minimum)
        self.maximum = int(maximum)

    def intersection(self, other):
        minimum = max(self.minimum, other.minimum)
        maximum = min(self.maximum, other.maximum)
        return Range(minimum, maximum) if minimum <= maximum else None

    def has_overlap(self, other):
        return self.intersection(other) is not None

    def differences(self, other):
        if not self.has_overlap(other):
            return [self]
        diff = []
        if self.minimum < other.minimum:
            diff.append(Range(self.minimum, other.minimum - 1))
        if self.maximum > other.maximum:
            diff.append(Range(other.maximum + 1, self.maximum))
        return diff

    def __len__(self):
        return self.maximum - self.minimum + 1

    def __str__(self):
        return "<" + str(self.minimum) + ".." + str(self.maximum) + ">"


class Cuboid():
    def __init__(self, status: str, rangex: Range, rangey: Range, rangez: Range):
        self.value = 1 if status == "on" else 0
        self.rangex = rangex
        self.rangey = rangey
        self.rangez = rangez

    def total_value(self):
        return self.value * len(self.rangex) * len(self.rangey) * len(self.rangez)

    def has_overlap(self, other):
        return self.rangex.has_overlap(other.rangex) and self.rangey.has_overlap(other.rangey) and self.rangez.has_overlap(other.rangez)

    def differences(self, other):
        if not self.has_overlap(other):
            return [self]

        diff = []
        for d_x in self.rangex.differences(other.rangex):
            diff.append(Cuboid(self.value, d_x, self.rangey, self.rangez))
        remaining_x = self.rangex.intersection(other.rangex)

        for d_y in self.rangey.differences(other.rangey):
            diff.append(Cuboid(self.value, remaining_x, d_y, self.rangez))
        remaining_y = self.rangey.intersection(other.rangey)

        for d_z in self.rangez.differences(other.rangez):
            diff.append(Cuboid(self.value, remaining_x, remaining_y, d_z))

        print("Differences:", len(diff))
        return diff

    def __str__(self):
        string = "Status: " + str(self.value)
        string += " X=" + str(self.rangex)
        string += " Y=" + str(self.rangey)
        string += " Z=" + str(self.rangez)
        return(string)


def parse_input(input: List[str]) -> List:
    cuboids = []
    for line in input:
        status, coords = line.split(" ")
        cuboid = [c.split('=')[1].split('..') for c in coords.split(',')]
        cuboids.append(Cuboid(status, Range(cuboid[0][0], cuboid[0][1]), Range(cuboid[1][0], cuboid[1][1]), Range(cuboid[2][0],cuboid[2][1])))

    return cuboids


def useLimitedGrid(cuboids: List[Cuboid], region_limit: int) -> set:
    grid = set()
    for cuboid in cuboids:
        for x in range(max(cuboid.rangex.minimum, -region_limit), min(cuboid.rangex.maximum, region_limit)+1):
            for y in range(max(cuboid.rangey.minimum, -region_limit), min(cuboid.rangey.maximum, region_limit)+1):
                for z in range(max(cuboid.rangez.minimum, -region_limit), min(cuboid.rangez.maximum, region_limit)+1):
                    if cuboid.value:
                        grid.add((x, y, z))
                    elif (x, y, z) in grid:
                        grid.remove((x, y, z))
    return grid


def combine(cuboids: List[Cuboid], new_cuboid: Cuboid) -> List[Cuboid]:
    remaining = []
    print("Combining:", new_cuboid)
    for cuboid in cuboids:
        remaining += cuboid.differences(new_cuboid)
        print("Remaining:", len(remaining))

    return remaining + [new_cuboid]


def useUnlimitedGrid(cuboids: List[Cuboid]) -> List[Cuboid]:
    combinedCuboids = []
    for cuboid in cuboids:
        print("Current value PRE:", sum([cub.total_value() for cub in combinedCuboids]))
        combinedCuboids = combine(combinedCuboids, cuboid)
        print("Current value POS:", sum([cub.total_value() for cub in combinedCuboids]))

    return combinedCuboids


with open("2021/day-22/example.txt") as f:
    cuboids = parse_input([str(line.strip()) for line in f])
    grid = useLimitedGrid(cuboids, 50)
    assert 39 == len(grid)
    cuboids = useUnlimitedGrid(cuboids)
    total_value = sum([cuboid.total_value() for cuboid in cuboids])
    print("Total value:", total_value)
    assert 39 == total_value

with open("2021/day-22/larger-example.txt") as f:
    cuboids = parse_input([str(line.strip()) for line in f])
    grid = useLimitedGrid(cuboids, 50)
    assert 590784 == len(grid)

with open("2021/day-22/largest-example.txt") as f:
    cuboids = parse_input([str(line.strip()) for line in f])
    grid = useLimitedGrid(cuboids, 50)
    assert 474140 == len(grid)

    cuboids = useUnlimitedGrid(cuboids)
    total_value = sum([cuboid.total_value() for cuboid in cuboids])
    print("Total value:", total_value)
    assert 2758514936282235 == total_value

with open("2021/day-22/input.txt") as f:
    steps = parse_input([str(line.strip()) for line in f])
    grid = useLimitedGrid(steps, 50)
    print("Part 1: The amount of cubes is:", len(grid))
#     print("Part 2: The amount of cubes is:", max(quantum_game.wins))
