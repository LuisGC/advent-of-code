from typing import List
from collections import defaultdict
from enum import Enum
from dataclasses import dataclass
from time import perf_counter

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took: " + "{:2.5f}".format(perf_counter() - t) + " sec") 
        return ret
    
    return wrapper_method

@dataclass(frozen=True)
class Position2D:
    row: int
    col: int

    def is_inside_grid(self, grid):
        r, c = self.row, self.col
        return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[r])

    def iter_neighbors(self, cardinal=True):
        if cardinal:
            for d in Direction:
                yield self + d
        else:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr != 0 or dc != 0:
                        yield self + Position2D(dr, dc)
    def __add__(self, other):
        p0 = self if not isinstance(self, Direction) else self.value
        r0, c0 = p0.row, p0.col

        p1 = other if not isinstance(other, Direction) else other.value
        r1, c1 = p1.row, p1.col

        return Position2D(r0+r1, c0+c1)
    def __getitem__(self, index):
        return (self.row, self.col)[index]

class Direction(Enum):
    LEFT = Position2D(0, -1)
    RIGHT = Position2D(0, 1)
    UP = Position2D(-1, 0)
    DOWN = Position2D(1, 0)

@profiler
def longest_hike(input_lines: List[str]) -> int:

    memo = defaultdict(lambda: -1)

    queue = [(Position2D(0, 1), set(), 0)] # position, visited, steps

    while queue:
        current, queue = queue[0], queue[1:]
        position, visited, steps = current

        memo[position] = steps
        row, col = position

        dirs = [dir for dir in Direction]

        if input_lines[row][col] == ">":
            dirs = [Direction.RIGHT]
        elif input_lines[row][col] == "<":
            dirs = [Direction.LEFT]
        elif input_lines[row][col] == "^":
            dirs = [Direction.UP]
        elif input_lines[row][col] == "v":
            dirs = [Direction.DOWN]
        
        for new_dir in dirs:
            new_row, new_col = new_pos = position + new_dir
            if (new_pos not in visited and
                0 <= new_row < len(input_lines) and 0 <= new_col < len(input_lines[0]) and
                input_lines[new_row][new_col] != "#" and
                memo[position] < steps + 1):
                queue.append((new_pos, visited | {position}, steps + 1))

    return memo[Position2D((len(input_lines)-1), len(input_lines[-1])-2)]

@profiler
def longest_hike_without_slopes(input_lines: List[str]) -> int:

    start = Position2D(0, 1)
    end = Position2D(len(input_lines)-1, len(input_lines[-1])-2)

    graph = dict()
    for r, row in enumerate(input_lines):
        for c, char in enumerate(row):
            if char != "#":
                pos = Position2D(r, c)
                neighbours = defaultdict(int)
                for new_pos in pos.iter_neighbors():
                    if (new_pos.is_inside_grid(input_lines) and 
                        input_lines[new_pos.row][new_pos.col] != "#"):
                        neighbours[new_pos] = 1
                graph[pos] = neighbours

    for pos in list(graph.keys()):
        neighbours = graph[pos]
        if len(neighbours) == 2:
            a, b = neighbours.keys()
            del graph[a][pos]
            del graph[b][pos]
            graph[b][a] = graph[a][b] = max(graph[a][b], neighbours[a] + neighbours[b])
            del graph[pos]

    visited = {start: 0}
    def dfs(pos: Position2D) -> int:
        if pos == end:
            return sum(visited.values())
        max_steps = 0
        for new_pos in graph[pos]:
            if new_pos not in visited:
                visited[new_pos] = graph[pos][new_pos]
                max_steps = max(max_steps, dfs(new_pos))
                del visited[new_pos]
        return max_steps
    
    return dfs(start)

with open("2023/day-23/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    
    assert 94 == longest_hike(input_lines)
    assert 154 == longest_hike_without_slopes(input_lines)

with open("2023/day-23/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    
    print("Part 1: The longest hike is ", longest_hike(input_lines))
    print("Part 2: The longest hike without slopes is ", longest_hike_without_slopes(input_lines))
    