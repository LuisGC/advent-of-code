from __future__ import annotations
from typing import List
import re

class Valve:
    id: str
    flow_rate: int
    neighbors: List
    distances: dict

    def __init__(self, id, flow_rate, neighbors):
        self.id = id
        self.flow_rate = flow_rate
        self.neighbors = neighbors
        self.distances = {}

    def __str__(self):
        return f"  Valve {self.id} has flow rate= {self.flow_rate} and neighbors: {self.neighbors}"

    def distance(self, destination) -> int:
        return self.distances[destination]

    @staticmethod
    def parse_valve(line: str) -> Valve:
        match = re.search(r'Valve (\S+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)$', line)
        if match is None: raise Exception(f"no match with {line}")

        id, flow_rate, destinations = match.groups()
        tunnels = list(map(lambda tunnel: tunnel.strip(), destinations.split(",")))

        return Valve(id, int(flow_rate), tunnels)

def parse_input(lines: List[str]) -> dict:
    valve_dict = {}
    for line in lines:
        valve = Valve.parse_valve(line)
        valve_dict[valve.id] = valve

    return valve_dict

def complete_data(valves: dict) -> List:
    non_zeros = []
    for valve in valves.values():
        fill_distances(valves, valve)
        if valve.flow_rate != 0:
            non_zeros.append(valve)

    return non_zeros

def fill_distances(valves: dict, valve = Valve):
    frontier = [valve.id]
    visited = [valve.id]
    distance = 0
    while frontier:
        distance += 1
        new_frontier = []
        for frontier_valve_id in frontier:
            frontier_valve = valves[frontier_valve_id]
            for neighbors_id in frontier_valve.neighbors:
                if neighbors_id not in visited and neighbors_id not in new_frontier:
                    visited.append(neighbors_id)
                    new_frontier.append(neighbors_id)
                    valve.distances[neighbors_id] = distance
        frontier = new_frontier


def get_paths(valves: dict, current: str, non_zeros: List[Valve], time: int, visited: List) -> List:
    paths = [[0]]
    for valve in non_zeros:
        if valve.id != current and valve.id not in visited:
            distance = valves[current].distances[valve.id]
            if distance + 1 < time:
                inner_paths = get_paths(valves, valve.id, non_zeros, time - (distance +1), visited + [valve.id])
                for path in inner_paths:
                    paths.append([valve.id] + path)

    return paths

def pressure_in_path(valves: dict, current: str, path: List, time: int) -> int:
    pressure = 0
    time_left = time
    curr = current
    for i in range(len(path)):
        next = path[i]
        time_left -= valves[curr].distance(next) + 1
        pressure += valves[next].flow_rate * time_left
        curr = next

    return pressure

def release_optimal_pressure(valves: dict, time: int = 30, current: str= 'AA') -> int:
    non_zeros = complete_data(valves)

    paths = get_paths(valves, current, non_zeros, time, [])
    paths = [path[:-1] for path in paths]
    pressures = [pressure_in_path(valves, current, path, time) for path in paths]

    return max(pressures)

def release_optimal_pressure_with_help(valves: dict, time: int = 26, current: str= 'AA') -> int:
    non_zeros = complete_data(valves)

    paths = get_paths(valves, current, non_zeros, time, [])
    paths = [path[:-1] for path in paths]
    pressures = [pressure_in_path(valves, current, path, time) for path in paths]

    best_combination = 0
    for path, pressure in zip(paths, pressures):
        if len(path) <= len(non_zeros) / 2:
            for path_2, pressure_2 in zip(paths, pressures):
                if len(path_2) <= len(non_zeros) - len(path):
                    if set(path).isdisjoint(path_2):
                        best_combination = max(best_combination, pressure + pressure_2)

    return best_combination

with open("2022/day-16/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    input_valves = parse_input(input_lines)
    
    assert 1651 == release_optimal_pressure(input_valves)
    assert 1707 == release_optimal_pressure_with_help(input_valves)

with open("2022/day-16/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    input_valves = parse_input(input_lines)
    
    print("Part 1: Optimal pressure is:", release_optimal_pressure(input_valves))
    # REFACTOR It takes too long to finish, but it finishes
    print("Part 2: Optimal pressure with help is:", release_optimal_pressure_with_help(input_valves))
