from typing import List, Tuple

MAZE_RULES = {
    ("L", 1j): 1, ("L", -1): -1j,
    ("J", 1j): -1, ("J", 1): -1j,
    ("7", 1): 1j, ("7", -1j): -1,
    ("F", -1): 1j, ("F", -1j): 1
}

def starting_position(input_lines: List[str]) -> complex:
    return [complex(j, i) for i, row in enumerate(input_lines) for j, char in enumerate(row) if char == "S"][0]

def distance_and_track(maze: List[str], start: complex, dir: int = 1) -> Tuple[int, List[complex]]:
    pos = start + dir
    track = [pos]
    s = 1

    while pos != start:
        x, y = int(pos.real), int(pos.imag)
        if maze[y][x] not in ["|", "-"]:
            dir = MAZE_RULES[(maze[y][x], dir)]
        
        pos += dir
        track.append(pos)
        s += 1

    return (s // 2), track


def clean_maze_with_track(maze: List[str], track: List[complex], initial: str) -> List[str]:
    clean_maze = {}
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "." or (complex(x, y) in track):
                if char == "S":
                    clean_maze[(x, y)] = initial
                else:
                    clean_maze[(x, y)] = char
            else:
                # not in track
                clean_maze[(x, y)] = "."

    return clean_maze


def tiles_enclosed(maze: dict, rows: int, cols: int) -> int:
    enclosed = 0
    for y in range(rows):
        inside = False
        last_corner = None
        for x in range(cols):
            pipe = maze.get((x,y))
            if pipe == ".":
                if inside:
                    enclosed += 1
            elif pipe == "|":
                assert last_corner is None
                inside = not inside
            elif pipe == "-":
                continue
            else:
                if last_corner is None:
                    assert pipe in ("L", "F")
                    last_corner = "N" if pipe in ("L", "J") else "S"
                else:
                    assert pipe in ("J", "7")
                    this_corner = "N" if pipe in ("L", "J") else "S"
                    if last_corner != this_corner:
                        # equivalent to another |
                        inside = not inside
                    last_corner = None

    return enclosed


with open("2023/day-10/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    distance, track = distance_and_track(input_lines, starting_position(input_lines))
    assert 4 == distance

with open("2023/day-10/example2.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    distance, track = distance_and_track(input_lines, starting_position(input_lines))
    assert 8 == distance
    
with open("2023/day-10/example-enclosed-1.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    distance, track = distance_and_track(input_lines, starting_position(input_lines))
    assert 23 == distance
    clean_maze = clean_maze_with_track(input_lines, track, "F")
    assert 4 == tiles_enclosed(clean_maze, rows=len(input_lines), cols=len(input_lines[0]))

with open("2023/day-10/example-enclosed-2.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    distance, track = distance_and_track(input_lines, starting_position(input_lines))
    assert 70 == distance
    clean_maze = clean_maze_with_track(input_lines, track, "F")
    assert 8 == tiles_enclosed(clean_maze, rows=len(input_lines), cols=len(input_lines[0]))

with open("2023/day-10/example-enclosed-3.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    distance, track = distance_and_track(input_lines, starting_position(input_lines), -1)
    assert 80 == distance
    clean_maze = clean_maze_with_track(input_lines, track, "7")
    assert 10 == tiles_enclosed(clean_maze, rows=len(input_lines), cols=len(input_lines[0]))

with open("2023/day-10/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    distance, track = distance_and_track(input_lines, starting_position(input_lines), -1)
    print("Part 1: The farthest distance is ", distance)
    clean_maze = clean_maze_with_track(input_lines, track, "J")
    print("Part 2: Number of tiles enclosed is ", tiles_enclosed(clean_maze, rows=len(input_lines), cols=len(input_lines[0])))
