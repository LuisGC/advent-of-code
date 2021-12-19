from typing import List
from itertools import permutations, product
from collections import Counter
from numpy import abs

class Scanner:
    def __init__(self, block: str):
        lines = block.splitlines()
        self.id = lines[0].split(" ")[2]
        self.coords = [[int(x) for x in l.split(',')] for l in lines[1:]]
        self.position = None

    def __str__(self):
        string = "ID: " + str(self.id)
        string += " Position: " + str(self.position)
        return(string)


def reorient_iterator():
	for rotation in permutations([0,1,2]):
		for orientation in product([1,-1], repeat=3):
			yield lambda coord: (orientation[0] * coord[rotation[0]], orientation[1] * coord[rotation[1]], orientation[2] * coord[rotation[2]])


def print_scanners(scanners: List[Scanner]):
    for s in scanners:
        print(s)
    print("\n")


def parse_input(blocks: List) -> List:
    scanners = [Scanner(block) for block in blocks]
    return scanners


def locate_objects(scanners: List[Scanner]) -> List:

    scanners[0].position = [0,0,0]
    coords = {(x,y,z):"B" for x,y,z in scanners[0].coords}
    coords[(0,0,0)] = "S"

    while any(s.position is None for s in scanners):
        for scanner in scanners:
            if scanner.position is None:
                for reorient in reorient_iterator():
                    new_scanner = map(reorient, scanner.coords)
                    diffs = Counter()

                    for xb,yb,zb in new_scanner:
                        for xa,ya,za in coords:
                            diffs[xa-xb, ya-yb, za-zb] += 1
                    if any(d >= 12 for d in diffs.values()):
                        diff = next(d for d in diffs if diffs[d] >= 12)
                        for x,y,z in map(reorient, scanner.coords):
                            coords[x+diff[0],y+diff[1],z+diff[2]] = "B"
                            coords[diff] = "S"
                            scanner.position = diff

    return coords, scanners


def count_beacons(coords: dict) -> int:
    return sum(c == "B" for c in coords.values())


def max_distance(scanners: List[Scanner]) -> int:
    max_d = 0
    for s1, s2 in permutations(scanners, 2):
        distance = abs(s1.position[0] - s2.position[0]) + abs(s1.position[1] - s2.position[1]) + abs(s1.position[2] - s2.position[2])
        max_d = max(max_d, distance)
    return max_d


with open("2021/day-19/example.txt") as f:
    scanners = parse_input(f.read().split("\n\n"))
    coords, scanners = locate_objects(scanners)
    assert 79 == count_beacons(coords)
    assert 3621 == max_distance(scanners)

with open("2021/day-19/input.txt") as f:
    scanners = parse_input(f.read().split("\n\n"))
    coords, scanners = locate_objects(scanners)
    print("Part 1: The amount of beacons is:", count_beacons(coords))
    print("Part 2: Max distance between any two scanners is:", max_distance(scanners))
