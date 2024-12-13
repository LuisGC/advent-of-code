import sys
from typing import List, Tuple
from time import perf_counter
sys.path.insert(0, './')
from utils import DIRECTIONS

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took: " + "{:2.5f}".format(perf_counter() - t) + " sec") 
        return ret
    
    return wrapper_method

def calculate_full_price(regions: List) -> int:
    price = 0
    for region in regions:
        area = len(region)
        perimeter = 0
        for plot in region:
            for xOff, yOff, in DIRECTIONS:
                if (plot[0] + xOff, plot[1] + yOff) not in region:
                    perimeter += 1
        price += area * perimeter
    return price

def calculate_bulk_price(regions: List) -> int:
    price = 0
    for region in regions:
        area = len(region)
        sides = 0
        visited = set()
        for plot in region:
            for side in DIRECTIONS:
                if (plot[0] + side[0], plot[1] + side[1]) in region or (plot, side) in visited:
                    continue
                sides += 1
                for dir in DIRECTIONS:
                    if abs(side[0]) == abs(dir[0]) and abs(side[1] == abs(dir[1])):
                        continue
                    x, y = plot
                    while (x, y) in region and (x + side[0], y + side[1]) not in region:
                        visited.add(((x,y), side))
                        x, y = x + dir[0], y + dir[1]
        price += area * sides

    return price

@profiler
def calculate_total_price(plantmap: List) -> Tuple[int, int]:
    heigth = len(plantmap)
    width = len(plantmap[0])

    regions = []
    def findregion(plantmap: List[str], region: set, x: int, y: int):
        if any(r for r in regions if r == (x,y)) or (x, y) in region:
            return
        region.add((x, y))
        for xOff, yOff, in DIRECTIONS:
            if x + xOff < 0 or y + yOff < 0 or x+xOff >= width or y + yOff >= heigth:
                continue
            if plantmap[y][x] == plantmap[y+yOff][x+xOff]:
                findregion(plantmap, region, x + xOff, y + yOff)

    for x in range(width):
        for y in range(heigth):
            region = set()
            findregion(plantmap, region, x, y)
            if len(region) > 0 and region not in regions:
                regions.append(region)

    return calculate_full_price(regions), calculate_bulk_price(regions)

with open("2024/day-12/example-abcde.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    full_price, bulk_price = calculate_total_price(input_lines)
    assert 140 == full_price
    assert 80 == bulk_price

with open("2024/day-12/example-ox.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    full_price, bulk_price = calculate_total_price(input_lines)
    assert 772 == full_price
    assert 436 == bulk_price

with open("2024/day-12/larger-example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    full_price, bulk_price = calculate_total_price(input_lines)
    assert 1930 == full_price
    assert 1206 == bulk_price

with open("2024/day-12/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    full_price, bulk_price = calculate_total_price(input_lines)

    print(f"Part 1: Total price of fending all regions is {full_price}")
    print(f"Part 2: Bulk price of fending all regions is {bulk_price}")
