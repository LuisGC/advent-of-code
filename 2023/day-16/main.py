from typing import List

directions = {
    0: (0, -1), # N
    1: (1, 0),  # E
    2: (0, 1),  # S
    3: (-1,0)   # W
}

def energize(contraption: List[str], start_x: int, start_y: int, start_dir: int) -> int:
    heigth = len(contraption)
    width = len(contraption[0])

    energized = set()
    seen = set()

    beams = [(start_x, start_y, start_dir)]

    while beams:
        beam = beams.pop()
        if beam in seen:
            continue
        else:
            seen.add(beam)

        beam_x, beam_y, beam_dir = beam

        next_x = beam_x + directions[beam_dir][0]
        next_y = beam_y + directions[beam_dir][1]

        if not (0 <= next_x < width and 0 <= next_y < heigth):
            continue

        energized.add((next_x, next_y))

        tile = contraption[next_y][next_x]

        if tile == '.' or (tile == '-' and beam_dir in [1, 3]) or (tile == '|' and beam_dir in [0, 2]):
            beams.append((next_x, next_y, beam_dir))
            continue
        elif tile == '-':
            beams.append((next_x, next_y, 1))
            beams.append((next_x, next_y, 3))
            continue
        elif tile == '|':
            beams.append((next_x, next_y, 0))
            beams.append((next_x, next_y, 2))
            continue
        elif tile == '/':
            if beam_dir in [0, 2]:
                beam_dir += 1
            else:
                beam_dir -= 1
        elif tile == '\\':
            if beam_dir == 0:
                beam_dir = 3
            elif beam_dir == 1:
                beam_dir = 2
            elif beam_dir == 2:
                beam_dir = 1
            elif beam_dir == 3:
                beam_dir = 0
        else:
            print("Unexpected tile", tile)

        beams.append((next_x, next_y, beam_dir))


    return len(energized)

def max_energize(contraption: List[str]) -> int:
    heigth = len(contraption)
    width = len(contraption[0])

    energized_options = []
    for y in range(heigth):
        energized_options.append(energize(contraption, start_x = -1, start_y = y, start_dir = 1))
        energized_options.append(energize(contraption, start_x = width, start_y = y, start_dir = 3))
    for x in range(width):
        energized_options.append(energize(contraption, start_x = x, start_y = -1, start_dir = 2))
        energized_options.append(energize(contraption, start_x = x, start_y = heigth, start_dir = 0))

    return max(energized_options)
        

with open("2023/day-16/example.txt", encoding="utf-8") as f:
    contraption = [line.strip() for line in f.readlines()]

    assert 46 == energize(contraption, start_x = -1, start_y = 0, start_dir = 1)
    assert 51 == max_energize(contraption)

with open("2023/day-16/input.txt", encoding="utf-8") as f:
    contraption = [line.strip() for line in f.readlines()]
    
    print("Part 1: The amount of energized tiles is ", energize(contraption, start_x = -1, start_y = 0, start_dir = 1))
    print("Part 2: The max amount of energized tiles is ", max_energize(contraption))