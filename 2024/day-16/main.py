import heapq
import sys
from itertools import product
from typing import List, Tuple
sys.path.insert(0, './')
from utils import profiler, DIRECTIONS

WALL = "#"

def h(position: Tuple[int, int], direction: Tuple[int, int], goal: Tuple[int, int]) -> int:
    i, j = position
    i_goal, j_goal = goal
    Δi, Δj = direction
    if Δj == 1:
        if i == i_goal:
            return j_goal - j
        else:
            return 1000 + (j_goal - j) + (i - i_goal)
    if Δi == -1:
        if j == j_goal:
            return i - i_goal
        else:
            return 1000 + (j_goal - j) + (i - i_goal)
        
    return 2000 + (j_goal - j) + (i - i_goal)

@profiler
def lowest_score(input_lines: List[str]) -> int:
    rows, cols = len(input_lines), len(input_lines[0])
    start, goal = (rows - 2, 1), (1, cols - 2)
    direction = (0, 1)
    cost = {start: 0}

    priority_queue = []
    heapq.heappush(priority_queue, (h(start, direction, goal), start, direction))

    while priority_queue:
        _, current, direction = heapq.heappop(priority_queue)

        if current == goal:
            return cost[current]
        
        i, j = current
        for Δi, Δj in DIRECTIONS:
            neighbor = (i + Δi, j + Δj)
            if input_lines[i + Δi][j + Δj] == WALL:
                continue

            if (Δi, Δj) == direction:
                tentative_cost = cost[current] + 1
            else:
                tentative_cost = cost[current] + 1001

            if neighbor not in cost or tentative_cost < cost[neighbor]:
                cost[neighbor] = tentative_cost
                heapq.heappush(
                    priority_queue,
                    (cost[neighbor] + h(neighbor, (Δi, Δj), goal),
                     neighbor,
                     (Δi, Δj)),
                )

@profiler
def seats(input_lines: List[str]) -> int:
    rows, cols = len(input_lines), len(input_lines[0])
    start, goal = (rows - 2, 1), (1, cols - 2)
    direction = (0, 1)
    cost = {(start, direction): 0}

    priority_queue = []
    heapq.heappush(priority_queue, (h(start, direction, goal), start, direction))

    while priority_queue:
        _, current, direction = heapq.heappop(priority_queue)
        i, j = current
        Δi, Δj = direction

        # compute neighbors
        neighbors = [((i + Δi, j + Δj), direction, 1)]
        for dir in DIRECTIONS:
            if dir != direction:
                neighbors.append((current, dir, 1000))

        # explore neighbors
        for n in neighbors:
            n_i, n_j = n[0]
            if input_lines[n_i][n_j] == WALL:
                continue

            tentative_cost = cost[(current, direction)] + n[2]

            if (n[0], n[1]) not in cost or tentative_cost < cost[(n[0], n[1])]:
                cost[(n[0], n[1])] = tentative_cost
                heapq.heappush(
                    priority_queue,
                    (
                        cost[(n[0], n[1])] + h(n[0], n[1], goal),
                        n[0],
                        n[1]
                    )
                )
    
    back = {(goal, (0 , 1)): 0, (goal, (-1, 0)): 0}
    pq = []
    heapq.heappush(pq, (0, goal, (0, 1)))
    heapq.heappush(pq, (0, goal, (-1, 0)))

    while pq:
        _, current, direction = heapq.heappop(pq)
        i, j = current
        Δi, Δj = direction

        # compute neighbors
        neighbors = [((i - Δi, j - Δj), direction, 1)]
        for dir in DIRECTIONS:
            if dir != direction:
                neighbors.append((current, dir, 1000))

        # explore neighbors
        for n in neighbors:
            n_i, n_j = n[0]
            if input_lines[n_i][n_j] == WALL:
                continue

            tentative_cost = back[(current, direction)] + n[2]

            if (n[0], n[1]) not in back or tentative_cost < back[(n[0], n[1])]:
                back[(n[0], n[1])] = tentative_cost
                heapq.heappush(pq, (back[(n[0], n[1])], n[0], n[1]))
    
    total = min(cost[(goal, (-1, 0))], cost[(goal, (0, 1))])

    seats = set()
    for i, j in product(range(rows), range(cols)):
        for dir in DIRECTIONS:
            if (
                ((i, j), dir) in cost
                and ((i, j), dir) in back
                and cost[((i, j), dir)] + back[((i, j), dir)] == total
            ):
                seats.add((i, j))

    return len(seats)
          

with open("2024/day-16/example.txt", encoding="utf-8") as f:
    maze = [line.strip() for line in f.readlines()]
    assert 7036 == lowest_score(maze)
    assert 45 == seats(maze)

with open("2024/day-16/example-2.txt", encoding="utf-8") as f:
    maze = [line.strip() for line in f.readlines()]
    assert 11048 == lowest_score(maze)
    assert 64 == seats(maze)

with open("2024/day-16/input.txt", encoding="utf-8") as f:
    maze = [line.strip() for line in f.readlines()]

    print(f"Part 1: Lowest score is {lowest_score(maze)}")
    print(f"Part 2: Amount of tiles at least in one of the best paths is {seats(maze)}")