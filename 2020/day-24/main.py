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


def artistic_flip(layout: Dict, times: int) -> Dict:

    for _ in range(times):
        opts = set((x + dx, y + dy)
                   for x, y in layout.keys()
                   for dx, dy in directions.values())
        new_state = defaultdict(int)
        for x, y in opts:
            old = layout[(x, y)]
            adj = sum(layout[x + dx, y + dy]
                      for dx, dy in directions.values())
            if old == 1 and adj not in [1, 2]:
                new_state[x, y] = 0
            elif old == 0 and adj == 2:
                new_state[x, y] = 1
            else:
                new_state[x, y] = old

        layout = new_state

    return layout


def count_black_tiles(layout: Dict) -> int:
    return sum(v == 1 for v in layout.values())


with open("2020/day-24/example.txt", encoding="utf-8") as f:
    tile_layout = flip_tiles(f.readlines())
    assert 10 == count_black_tiles(tile_layout)
    assert 15 == count_black_tiles(artistic_flip(tile_layout, 1))
    assert 12 == count_black_tiles(artistic_flip(tile_layout, 2))
    assert 25 == count_black_tiles(artistic_flip(tile_layout, 3))
    assert 23 == count_black_tiles(artistic_flip(tile_layout, 5))
    assert 37 == count_black_tiles(artistic_flip(tile_layout, 10))
    assert 566 == count_black_tiles(artistic_flip(tile_layout, 50))
    assert 2208 == count_black_tiles(artistic_flip(tile_layout, 100))


with open("2020/day-24/input.txt", encoding="utf-8") as f:
    tile_layout = flip_tiles(f.readlines())
    print("Part 1: The amount of tiles with the black side up is: ",
          count_black_tiles(tile_layout))
    print('''Part 2: The amount of tiles with the black side up
            after 100 days of artistic flips is: ''',
          count_black_tiles(artistic_flip(tile_layout, 100)))
