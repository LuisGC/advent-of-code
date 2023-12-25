from typing import List
from math import prod
from networkx import Graph, connected_components, minimum_edge_cut
from time import perf_counter

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print("Method " + method.__name__ + " took: " + "{:2.5f}".format(perf_counter() - t) + " sec") 
        return ret
    
    return wrapper_method


def parse_input(lines: List[str]) -> Graph:
    g = Graph()
    for line in lines:
        name, others = line.split(": ")
        for other in others.split():
            g.add_edge(name, other)

    return g

@profiler
def disconnect_half_equipment(lines: List[str]) -> int:
    graph = parse_input(input_lines)
    graph.remove_edges_from(minimum_edge_cut(graph))

    return prod(len(comp) for comp in connected_components(graph))

with open("2023/day-25/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 54 == disconnect_half_equipment(input_lines)

with open("2023/day-25/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    print("Part 1: The product of the sizes is ", disconnect_half_equipment(input_lines))
