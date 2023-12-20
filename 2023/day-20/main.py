from time import perf_counter
from typing import List, Tuple, Dict

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
    for line in lines:
        module = Module(line)
        modules[module.name] = module
    
    for module in modules:
        if modules[module].type == "&":
            modules[module].input = {}
            for dest in modules:
                if module in modules[dest].next:
                    modules[module].input[dest] = False

    return modules


@profiler
def total_pulses(modules: dict) -> int:
    highs = 0
    lows = 0

    for _ in range(1000):
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

with open("2023/day-20/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    modules = parse_input(input_lines)

    assert 32000000 == total_pulses(modules)

with open("2023/day-20/example-2.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    modules = parse_input(input_lines)

    assert 11687500 == total_pulses(modules)

with open("2023/day-20/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    modules = parse_input(input_lines)
    
    print("Part 1: The total pulses prod is ", total_pulses(modules))