from time import perf_counter
from typing import List
from math import lcm


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took: " + "{:2.5f}".format(perf_counter() - t) + " sec") 
        return ret
    
    return wrapper_method

class Module:
    def __init__(self, line: str) -> None:
        parts = line.split(" -> ")
        self.name = parts[0]
        if parts[0][0] in "%&":
            self.type = parts[0][0]
            self.name = "".join(parts[0][1:])
        else:
            self.type = ""
            self.name = parts[0]
        self.next = parts[1].split(", ")
        self.state = False

def parse_input (lines: List[str]) -> dict:
    modules = {}
    key_module = None
    for line in lines:
        module = Module(line)
        modules[module.name] = module

        if "rx" in module.next:
            key_module = module.name

    for module in modules:
        if modules[module].type == "&":
            modules[module].input = {}
            for dest in modules:
                if module in modules[dest].next:
                    modules[module].input[dest] = False

    return modules, key_module

@profiler
def total_pulses(modules: dict, limit: int = 1000) -> int:
    highs = 0
    lows = 0

    for _ in range(limit):
        pending = [("broadcaster", False)]

        while pending:
            source, signal = pending.pop(0)

            dest = []
            output = signal

            if signal:
                highs += 1
            else:
                lows += 1

            if source in modules and modules[source].type == "":
                dest = modules[source].next
            elif source in modules and modules[source].type == "%" and not signal:
                output = modules[source].state = not modules[source].state
                dest = modules[source].next
            elif source in modules and modules[source].type == "&":
                output = not all(modules[source].input.values())
                dest = modules[source].next

            for d in dest:
                pending.append((d, output))
                if d in modules and modules[d].type == "&":
                    modules[d].input[source] = output

    return highs * lows

@profiler
def fewest_pulses(modules: dict, key_module: str = None) -> int:

    if key_module in modules:
        cycles = {m:0 for m in modules[key_module].input}

    cycle_count = 0
    while not all(cycles.values()):
        cycle_count += 1
        pending = [("broadcaster", False)]

        while pending:
            source, signal = pending.pop(0)

            dest = []
            output = signal

            if source in modules and modules[source].type == "":
                dest = modules[source].next
            elif source in modules and modules[source].type == "%" and not signal:
                output = modules[source].state = not modules[source].state
                dest = modules[source].next
            elif source in modules and modules[source].type == "&":
                output = not all(modules[source].input.values())
                dest = modules[source].next

                if source == key_module and any(modules[source].input.values()):
                    for module in modules[source].input:
                        if modules[source].input[module]:
                            cycles[module] = cycle_count

            for d in dest:
                pending.append((d, output))
                if d in modules and modules[d].type == "&":
                    modules[d].input[source] = output

    return lcm(*cycles.values())

with open("2023/day-20/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    modules, _ = parse_input(input_lines)
    assert 32000000 == total_pulses(modules)

with open("2023/day-20/example-2.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    modules, _ = parse_input(input_lines)
    assert 11687500 == total_pulses(modules)

with open("2023/day-20/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    
    modules, _ = parse_input(input_lines)
    print("Part 1: The total pulses prod is ", total_pulses(modules))

    modules, key_module = parse_input(input_lines)
    print("Part 2: The fewest number of pulses is ", fewest_pulses(modules, key_module))