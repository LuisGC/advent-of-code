from typing import List
from time import perf_counter

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took: " + "{:2.5f}".format(perf_counter() - t) + " sec") 
        return ret
    
    return wrapper_method

def calculate_price(regions) -> int:
    price = 0
    for region in regions:
        area = len(region)
        perimeter = 0
        for plot in region:
            for xOff, yOff, in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                if (plot[0] + xOff, plot[1] + yOff) not in region:
                    perimeter += 1
        price += area * perimeter
    return price

@profiler
def calculate_total_price(plantmap: List) -> int:
    heigth = len(plantmap)
    width = len(plantmap[0])

    regions = []

    def findregion(plantmap: List[str], region: set, x: int, y: int):
        if any(r for r in regions if r == (x,y)) or (x, y) in region:
            return
        region.add((x, y))
        for xOff, yOff, in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
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

    return calculate_price(regions)

with open("2024/day-12/example-abcde.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 140 == calculate_total_price(input_lines)

with open("2024/day-12/example-ox.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 772 == calculate_total_price(input_lines)

with open("2024/day-12/larger-example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 1930 == calculate_total_price(input_lines)

with open("2024/day-12/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: Total price of fending all regions is {calculate_total_price(input_lines)}")
#    print(f"Part 2: X-MAS found times is {count_X_MAS(input_lines)}")