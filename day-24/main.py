from typing import List, Dict
from collections import defaultdict

directions = {"e": (1, 0), "w": (-1, 0),
              "se": (0, 1), "sw": (-1, 1),
              "ne": (1, -1), "nw": (0, -1)}


def flip_tiles(transitions: List[str]) -> Dict:

    layout = defaultdict(int)

    for line in transitions:
        line = line.strip()
        i = 0
        x, y = 0, 0
        while i < len(line):
            if line[i] in directions:
                dx, dy = directions[line[i]]
                i += 1
            else:
                dx, dy = directions[line[i:i+2]]
                i += 2
            x, y = x + dx, y + dy

        layout[(x, y)] ^= 1

    return layout


def count_black_tiles(layout: Dict) -> int:
    return sum(v == 1 for v in layout.values())


with open("day-24/example.txt") as f:
    tile_layout = flip_tiles(f.readlines())
    assert 10 == count_black_tiles(tile_layout)


with open("day-24/input.txt") as f:
    tile_layout = flip_tiles(f.readlines())
    print("Part 1: The amount of tiles with the black side up is: ",
          count_black_tiles(tile_layout))
