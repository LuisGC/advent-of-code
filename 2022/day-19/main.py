from __future__ import annotations
import functools
import sys
import re
from typing import List
from math import prod

sys.setrecursionlimit(100000000)

class Blueprint:
    id: int
    ore: int
    clay: int
    obsidian: tuple
    geode: tuple
    
    def __init__(self, id: int, ore: int, clay: int, obsidian: tuple[int, int], geode:tuple[int, int]):
        self.id = id
        self.ore = ore
        self.clay = clay
        self.obsidian = (obsidian[0], obsidian[1])
        self.geode = (geode[0], geode[1])
        self.max_ore_robots = max(ore, clay, obsidian[0], geode[0])
        self.max_clay_robots = obsidian[1]
        self.max_obsidian_robots = geode[1]
    
    def __str__(self) -> str:
        return(f"Blueprint {self.id}:\n Each ore robot costs {self.ore} ore.\n Each clay robot costs {self.clay} ore.\n Each obsidian robot costs {self.obsidian[0]} ore and {self.obsidian[1]} clay.\n Each geode robot costs {self.geode[0]} ore and {self.geode[1]} obsidian.")

    @staticmethod
    def parse_blueprint(line: str) -> Blueprint:
        match = re.search(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line)
        if match is None: raise Exception(f"no match with {line}")
        id, ore, clay, obsidian_cost_ore, obsidian_cost_clay, geode_cost_ore, geode_cost_obsidian = match.groups()
        return Blueprint(int(id), int(ore), int(clay), (int(obsidian_cost_ore), int(obsidian_cost_clay)), (int(geode_cost_ore), int(geode_cost_obsidian)))

def parse_input(lines: list[str]) -> List[Blueprint]:
    blueprints = []
    for line in lines:
        blueprint = Blueprint.parse_blueprint(line)
        blueprints.append(blueprint)
    
    return blueprints

@functools.lru_cache(maxsize=None)
def mining(
    blueprint: Blueprint,
    max_time: int,
    minute: int = 1,
    ore: int = 0,
    clay: int = 0,
    obsidian: int = 0,
    geode: int = 0,
    ore_robots: int = 1,
    clay_robots: int = 0,
    obsidian_robots: int = 0,
    geode_robots: int = 0
) -> int:

    if minute > max_time:
        return geode

    # limiting the state space using the max of each resource we could use
    ore = min((max_time + 1 - minute) * blueprint.max_ore_robots, ore)
    clay = min((max_time + 1 - minute) * blueprint.max_clay_robots, clay)
    obsidian = min((max_time + 1 - minute) * blueprint.max_obsidian_robots, obsidian)

    options = []

    if ore >= blueprint.geode[0] and obsidian >= blueprint.geode[1]:
        options.append(
            mining(
                blueprint,
                max_time,
                minute + 1,
                ore + ore_robots - blueprint.geode[0],
                clay + clay_robots,
                obsidian + obsidian_robots - blueprint.geode[1],
                geode + geode_robots,
                ore_robots,
                clay_robots,
                obsidian_robots,
                geode_robots + 1
            )
        )

    if obsidian_robots < blueprint.max_obsidian_robots and ore >= blueprint.obsidian[0] and clay >= blueprint.obsidian[1]:
        options.append(
            mining(
                blueprint,
                max_time,
                minute + 1,
                ore + ore_robots - blueprint.obsidian[0],
                clay + clay_robots - blueprint.obsidian[1],
                obsidian + obsidian_robots,
                geode + geode_robots,
                ore_robots,
                clay_robots,
                obsidian_robots + 1,
                geode_robots
            )
        )

    if clay_robots < blueprint.max_clay_robots and ore >= blueprint.clay:
        options.append(
            mining(
                blueprint,
                max_time,
                minute + 1,
                ore + ore_robots - blueprint.clay,
                clay + clay_robots,
                obsidian + obsidian_robots,
                geode + geode_robots,
                ore_robots,
                clay_robots + 1,
                obsidian_robots,
                geode_robots
            )
        )

    if ore_robots < blueprint.max_ore_robots and ore >= blueprint.ore:
        options.append(
            mining(
                blueprint,
                max_time,
                minute + 1,
                ore + ore_robots - blueprint.ore,
                clay + clay_robots,
                obsidian + obsidian_robots,
                geode + geode_robots,
                ore_robots + 1,
                clay_robots,
                obsidian_robots,
                geode_robots
            )
        )
    
    # There is always the option of not building anything
    options.append(
            mining(
                blueprint,
                max_time,
                minute + 1,
                ore + ore_robots,
                clay + clay_robots,
                obsidian + obsidian_robots,
                geode + geode_robots,
                ore_robots,
                clay_robots,
                obsidian_robots,
                geode_robots
            )
        )

    return max(options)

def total_quality_level(blueprints: List[Blueprint], max_time, quality_level: bool=True) -> int:
    qualities = {}
    total_geodes = []
    for blueprint in blueprints:
        geodes = mining(blueprint,max_time)

        qualities[blueprint.id] = blueprint.id * geodes
        total_geodes.append(geodes)
        print(f"Blueprint {blueprint.id}: {geodes} geodes obtained and quality is {blueprint.id * geodes}")

    if quality_level:
        return sum(qualities.values())
    else:
        return prod(total_geodes)

# REFACTOR? It takes too long to execute all the cases
with open("2022/day-19/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    blueprints = parse_input(input_lines)

    assert 33 == total_quality_level(blueprints, max_time=24)
    assert 56 == total_quality_level(blueprints[:1], max_time=32, quality_level=False)
    assert 62 == total_quality_level(blueprints[1:2], max_time=32, quality_level=False)
    assert 56*62 == total_quality_level(blueprints[:3], max_time=32, quality_level=False)

with open("2022/day-19/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    blueprints = parse_input(input_lines)
    
    print("Part 1: Total quality level is:", total_quality_level(blueprints, max_time=24))
    print("Part 2: Total geodes in first 3 is:", total_quality_level(blueprints[:3], 32, quality_level=False))
