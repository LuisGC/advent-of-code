from typing import List
import hashlib

def load(platform: List[List[str]]) -> int:
    weigth = 0
    for i, line in enumerate(platform):
        weigth += (len(platform)-i) * line.count('O')
    return weigth

def move_north(platform: List[List[str]]) -> List[List[str]]:
    while True:
        new_platform = platform.copy()
        moves = 0
        for i in range(1, len(platform)):
            for j, c in enumerate(platform[i]):
                if c == 'O' and platform[i - 1][j] == '.':
                    new_platform[i - 1][j] = 'O'
                    new_platform[i][j] = '.'
                    moves += 1
        platform = new_platform.copy()
        if moves == 0:
            break

    return platform

def move_west(platform: List[List[str]]) -> List[List[str]]:
    while True:
        new_platform = platform.copy()
        moves = 0
        for i in range(len(platform)):
            for j in range(1, len(platform[i])):
                c = platform[i][j]
                if c == 'O' and platform[i][j - 1] == '.':
                    new_platform[i][j - 1] = 'O'
                    new_platform[i][j] = '.'
                    moves += 1
        platform = new_platform.copy()
        if moves == 0:
            break

    return platform

def move_south(platform: List[List[str]]) -> List[List[str]]:
    while True:
        new_platform = platform.copy()
        moves = 0
        for i in range(len(platform) - 1):
            for j, c in enumerate(platform[i]):
                if c == 'O' and platform[i + 1][j] == '.':
                    new_platform[i + 1][j] = 'O'
                    new_platform[i][j] = '.'
                    moves += 1
        platform = new_platform.copy()
        if moves == 0:
            break

    return platform

def move_east(platform: List[List[str]]) -> List[List[str]]:
    while True:
        new_platform = platform.copy()
        moves = 0
        for i in range(len(platform)):
            for j, c in enumerate(platform[i][:-1]):
                if c == 'O' and platform[i][j + 1] == '.':
                    new_platform[i][j + 1] = 'O'
                    new_platform[i][j] = '.'
                    moves += 1
        platform = new_platform.copy()
        if moves == 0:
            break

    return platform

def tilt_and_weight(platform: List[List[str]]) -> int:
    platform = move_north(platform)
    return load(platform)

def get_hash(platform: List[List[str]]) -> str:
    platform_to_text = "".join([''.join(line) for line in platform])
    return hashlib.sha1(platform_to_text.encode("utf-8")).hexdigest()[:20]

def spin_cycle(platform: List[List[str]], cycles: int = 1000000000) -> int:
    cache = {}
    results = []
    for cycle in range(cycles):
        platform = move_north(platform)
        platform = move_west(platform)
        platform = move_south(platform)
        platform = move_east(platform)
        key = get_hash(platform)
        if key in cache.keys():
            first = cache[key][1]
            diff = cycle - first
            return results[(cycles - first - 1) % diff + first]
        weight = load(platform)
        cache[key] = (weight, cycle)
        results.append(weight)
    return results[-1]


with open("2023/day-14/example.txt", encoding="utf-8") as f:
    platform = [list(line.strip()) for line in f.readlines()]

    assert 136 == tilt_and_weight(platform)
    # assert 87 == spin_cycle(platform, 1)
    # assert 69 == spin_cycle(platform, 2)
    # assert 69 == spin_cycle(platform, 3)
    assert 64 == spin_cycle(platform)

with open("2023/day-14/input.txt", encoding="utf-8") as f:
    platform = [list(line.strip()) for line in f.readlines()]
    
    print("Part 1: The load on the north is ", tilt_and_weight(platform))
    print("Part 2: The load on the north after 1B tilts is ", spin_cycle(platform))
