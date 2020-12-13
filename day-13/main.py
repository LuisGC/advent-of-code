from typing import List


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


with open("day-13/example.txt") as f:
    notes = f.read()
    line1, line2 = notes.strip().split("\n")
    departure = int(line1)
    buses = [int(x) for x in line2.split(",") if x != "x"]
    earliest_bus, wait_time = find_earliest_bus(departure, buses)
    assert 295 == earliest_bus * wait_time

with open("day-13/input.txt") as f:
    notes = f.read()
    line1, line2 = notes.strip().split("\n")
    departure = int(line1)
    buses = [int(x) for x in line2.split(",") if x != "x"]
    earliest_bus, wait_time = find_earliest_bus(departure, buses)
    print("Part 1: The earliest wait * bus is", earliest_bus * wait_time)
