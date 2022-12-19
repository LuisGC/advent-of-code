from __future__ import annotations
from typing import List
import re

class Blueprint:
    id: int
    ore_cost: int
    clay_cost: int
    obsidian_cost: tuple
    geode_cost: tuple
    ore: int
    clay: int
    obsidian: int
    geode: int

    def __init__(self, id: int, ore_cost: int, clay_cost: int, obsidian_cost: tuple, geode_cost:tuple):
        self.id = id
        self.ore_cost = ore_cost
        self.clay_cost = clay_cost
        self.obsidian_cost = obsidian_cost
        self.geode_cost = geode_cost
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0
    
    def __str__(self) -> str:
        return(f"Blueprint {self.id}:\n Each ore robot costs {self.ore_cost} ore.\n Each clay robot costs {self.clay_cost} ore.\n Each obsidian robot costs {self.obsidian_cost[0]} ore and {self.obsidian_cost[1]} clay.\n Each geode robot costs {self.geode_cost[0]} ore and {self.geode_cost[1]} obsidian.")

    def quality_level(self) -> int:
        return self.id * self.geode

    @staticmethod
    def parse_blueprint(line: str) -> Blueprint:
        match = re.search(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line)

        if match is None: raise Exception(f"no match with {line}")

        id, ore_cost, clay_cost, obsidian_cost_ore, obsidian_cost_clay, geode_cost_ore, geode_cost_obsidian = match.groups()

        return Blueprint(int(id), int(ore_cost), int(clay_cost), (int(obsidian_cost_ore), int(obsidian_cost_clay)), (int(geode_cost_ore), int(geode_cost_obsidian)))

    def collect(self, duration: int):
        pass


def parse_input(lines: list[str]) -> List[Blueprint]:
    blueprints = []
    for line in lines:
        blueprint = Blueprint.parse_blueprint(line)
        blueprints.append(blueprint)
    
    return blueprints

def total_quality_level(blueprints: List[Blueprint]) -> int:
    total = 0
    for blueprint in blueprints:
        blueprint.collect(24)
        total += blueprint.quality_level()

    return total

with open("2022/day-19/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    blueprints = parse_input(input_lines)
    
    assert 33 == total_quality_level(blueprints)

# with open("2022/day-19/input.txt", encoding="utf-8") as f:
#     input_lines = [line.strip() for line in f.readlines()]
#     input_valves = parse_input(input_lines)
    
#     print("Part 1: Optimal pressure is:", release_optimal_pressure(input_valves))
