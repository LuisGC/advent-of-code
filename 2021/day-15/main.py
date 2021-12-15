from heapq import *

class ChitonGrid:
    def __init__(self, lines: [str], factor: int):
        self.grid = []
        for line in lines:
            self.grid.append([int(x) for x in line])

        self.tile_height = len(lines)
        self.tile_width = len(lines[0])
        self.total_height = len(lines) * factor
        self.total_width = len(lines[0]) * factor
        self.factor = factor

    def adjacent(self, x, y):
        adjacent = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
        return filter(lambda xy: 0 <= xy[0] < self.total_height and 0 <= xy[1] < self.total_width, adjacent)

    def BreadthFirstSearch(self):
        q = [(0, 0, 0)]
        visited = set()
        while q:
            steps, x, y  = heappop(q)
            if (x, y) not in visited:
                visited.add((x, y))
            else:
                continue

            if (x, y) == (self.total_height - 1, self.total_width - 1):
                return steps

            for new_x, new_y in self.adjacent(x, y):
                times = new_x // self.tile_height + new_y // self.tile_width

                x_modulo = new_x % self.tile_height
                y_modulo = new_y % self.tile_width

                new_val = 1 + (self.grid[x_modulo][y_modulo] + times - 1) % 9

                heappush(q, (steps + new_val, new_x, new_y))

    def __str__(self):
        string = ''
        for i in range(len(self.grid)):
            string += str(self.grid[i]) + '\n'

        return string


with open("2021/day-15/example.txt") as f:
    lines = [line.strip() for line in f]
    grid  = ChitonGrid(lines, 1)
    assert 40 == grid.BreadthFirstSearch()
    grid  = ChitonGrid(lines, 5)
    assert 315 == grid.BreadthFirstSearch()

with open("2021/day-15/input.txt") as f:
    lines = [line.strip() for line in f]
    grid  = ChitonGrid(lines, 1)
    print("Part 1: Lowest total risk of any path is:", grid.BreadthFirstSearch())
    grid  = ChitonGrid(lines, 5)
    print("Part 2: Lowest total risk of any path with factor 5 is:", grid.BreadthFirstSearch())
