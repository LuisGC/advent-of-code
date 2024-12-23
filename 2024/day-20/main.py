import sys
from typing import List, Tuple, Iterator, NamedTuple
sys.path.insert(0, './')
from utils import profiler, vector_direction_values

START, END, WALL, EMPTY = "SE#."

class Position(NamedTuple):
    x: int
    y: int

def parse_input(input_lines: List[str]) -> Tuple[List[str], Position, Position]:
    maze = []

    start = end = Position(0, 0)
    for y, line in enumerate(input_lines):
        line = line.strip()
        maze.append(line)
        if START in line:
            start = Position(line.index(START), y)
        elif END in line:
            end = Position(line.index(END), y)
    return maze, start, end

def neighbors(maze: List[str], current: Position) -> Iterator[Position]:
    for direction in vector_direction_values:
        neighbor = Position(current.x + direction.x, current.y + direction.y)
        if at_pos(maze, neighbor) != WALL:
            yield neighbor

def at_pos(maze: List[str], pos: Position) -> str | None:
    if 0 <= pos.x < len(maze[0]) and 0 <= pos.y < len(maze):
        return maze[pos.y][pos.x]

def maze_to_track(maze: List[str], start: Position, end: Position) -> dict[Position, int]:
    track = {}
    current = start
    i = 0
    while True:
        track[current] = i
        if current == end:
            break
        for neighbor in neighbors(maze, current):
            if neighbor not in track:
                current = neighbor
                break
        i += 1

    return track

def find_cheats(track: dict[Position, int], max_cheat_length: int = 2) -> Iterator[int]:
    for cheat_start, i in track.items():
        for dx in range(-max_cheat_length, max_cheat_length + 1):
            for dy in range(-(max_cheat_length - abs(dx)), max_cheat_length - abs(dx) + 1):
                cheat_end = Position(cheat_start.x + dx, cheat_start.y + dy)
                if cheat_end in track:
                    yield track.get(cheat_end, 0) - i - (abs(dx) + abs(dy))

@profiler
def find_cheats_by_cheat_length(track: dict[Position, int], max_cheat_length: int = 2, savings: int = 100) -> int:
    return sum(1 for save in find_cheats(track, max_cheat_length=max_cheat_length) if save >= savings)


with open("2024/day-20/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    maze, start, end = parse_input(input_lines)
    track = maze_to_track(maze, start, end)

    assert 1 == find_cheats_by_cheat_length(track, savings=64)

with open("2024/day-20/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    maze, start, end = parse_input(input_lines)
    track = maze_to_track(maze, start, end)

    print(f"Part 1: Cheats with more than 100 savings are {find_cheats_by_cheat_length(track)}")
    print(f"Part 2: Cheats with more than 100 savings, cheating more are {find_cheats_by_cheat_length(track, max_cheat_length=20)}")
