from typing import List
from itertools import combinations
from z3 import Real, Solver, sat
from time import perf_counter

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took: " + "{:2.5f}".format(perf_counter() - t) + " sec") 
        return ret
    
    return wrapper_method

def intersect(stone1: List[int], stone2: List[int]) -> int:
    x1, y1 = int(stone1[0]), int(stone1[1])
    vx1, vy1 = int(stone1[3]), int(stone1[4])
    x2, y2 = int(stone2[0]), int(stone2[1])
    vx2, vy2 = int(stone2[3]), int(stone2[4])

    try:
        u = (vy1 * (x1 - x2) - vx1 * (y1 - y2)) / (vx2 * vy1 - vx1 * vy2)
        t = (vy2 * (x2 - x1) - vx2 * (y2 - y1)) / (vx1 * vy2 - vx2 * vy1)
    except ZeroDivisionError:
        return None

    if u < 0 or t < 0:
        return None
    
    return (x1 + vx1 * t, y1 + vy1 * t)


@profiler
def count_collisions(input_lines: List[str], min: int, max: int) -> int:
    count = 0
    for pair in combinations(input_lines, 2):
        one, two = pair
        
        stone1 = one.replace(" @", ", ").split(", ")
        stone2 = two.replace(" @", ", ").split(", ")

        p = intersect(stone1, stone2)
        if p and all(c > min and c <= max for c in p):
            count += 1

    return count

@profiler
def sum_terminator_rock_coords(input_lines: List[str]) -> int:
    rock_pos = [Real('r%s' % i) for i in range(3)]
    rock_vel = [Real('rv%s' % i) for i in range(3)]
    s = Solver()

    for i in range(len(input_lines)):
        stone = input_lines[i].replace(" @", ", ").split(", ")
        t = Real('t%s' % i)
        for c in range(3):
            s.add(rock_pos[c] + t * rock_vel[c] == stone[c] + t * stone[3 + c])

    if s.check() == sat:
        m = s.model()
        return sum([int(str(m.evaluate(v))) for v in rock_pos])
    else:
        return None


with open("2023/day-24/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    
    assert 2 == count_collisions(input_lines, min=7, max=27)
    assert 47 == sum_terminator_rock_coords(input_lines)

with open("2023/day-24/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    
    print("Part 1: The amount of collisions is ", count_collisions(input_lines, min=200000000000000, max=400000000000000))
    print("Part 2: The sum of coords of the Terminator rock is ", sum_terminator_rock_coords(input_lines))
