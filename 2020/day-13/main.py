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

    bussIds = [(offset, int(id))
               for offset, id in enumerate(rawbuses.split(","))
               if id != "x"]

    time = 0
    step = 1
    matched_buses = set()
    found = False

    while not found:
        time += step
        for offset, bus_id in bussIds:
            if (time+offset) % bus_id != 0:
                found = False
                break
            else:
                found = True
                if bus_id not in matched_buses:
                    matched_buses.add(bus_id)
                    step = bus_id * step // gcd(bus_id, step)

    return time


with open("2020/day-13/example.txt") as f:
    notes = f.read()
    line1, line2 = notes.strip().split("\n")
    departure = int(line1)
    buses = [int(x) for x in line2.split(",") if x != "x"]
    earliest_bus, wait_time = find_earliest_bus(departure, buses)
    assert 295 == earliest_bus * wait_time
    assert 1068781 == earliest_match(line2)


with open("2020/day-13/input.txt") as f:
    notes = f.read()
    line1, line2 = notes.strip().split("\n")
    departure = int(line1)
    buses = [int(x) for x in line2.split(",") if x != "x"]
    earliest_bus, wait_time = find_earliest_bus(departure, buses)
    print("Part 1: The earliest wait multiplied by bus ID is",
          earliest_bus * wait_time)
    earliest_match = earliest_match(line2)
    assert 100000000000000 < earliest_match
    print("Part 2: The earliest match is", earliest_match)
