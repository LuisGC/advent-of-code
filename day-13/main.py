from typing import List
from math import gcd


def find_earliest_bus(departure: int, buses: List[int]):
    earliest_bus = 999
    earliest_wait = 999

    for bus in buses:
        times = (departure // bus) + 1
        wait = (times * bus) % departure

        if wait < earliest_wait:
            earliest_bus = bus
            earliest_wait = wait

    return earliest_bus, earliest_wait


def earliest_match(rawbuses: str):
    print(rawbuses)

    bussIds = [(offset, int(ids))
              for offset, ids in enumerate(rawbuses.split(","))
              if ids != "x"]
    print(bussIds)

    time = 0
    step = 1
    usedSteps = set()
    found = False

    while not found:
        time += step
        found = True
        for offset, bussId in bussIds:
            if (time+offset) % bussId != 0:
                found = False
                break
            else:
                if bussId not in usedSteps:
                    print(time, usedSteps)
                    usedSteps.add(bussId)
                    step = bussId * step // gcd(bussId, step)

    return time


with open("day-13/example.txt") as f:
    notes = f.read()
    line1, line2 = notes.strip().split("\n")
    departure = int(line1)
    buses = [int(x) for x in line2.split(",") if x != "x"]
    earliest_bus, wait_time = find_earliest_bus(departure, buses)
    assert 295 == earliest_bus * wait_time
    assert 1068781 == earliest_match(line2)


with open("day-13/input.txt") as f:
    notes = f.read()
    line1, line2 = notes.strip().split("\n")
    departure = int(line1)
    buses = [int(x) for x in line2.split(",") if x != "x"]
    earliest_bus, wait_time = find_earliest_bus(departure, buses)
    print("Part 1: The earliest wait * bus is", earliest_bus * wait_time)
    earliest_match = earliest_match(line2)
    assert 100000000000000 < earliest_match
    print("Part 2: The earliest match is", earliest_match)
