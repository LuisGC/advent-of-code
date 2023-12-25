from typing import List
from math import prod
from networkx import Graph, connected_components, minimum_edge_cut

def parse_input(lines: List[str]) -> Graph:
    g = Graph()
    for line in lines:
        name, others = line.split(": ")
        for other in others.split():
            g.add_edge(name, other)

    return g

with open("2023/day-25/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    graph = parse_input(input_lines)
    graph.remove_edges_from(minimum_edge_cut(graph))
    assert 54 == prod(len(comp) for comp in connected_components(graph))

with open("2023/day-25/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    graph = parse_input(input_lines)
    graph.remove_edges_from(minimum_edge_cut(graph))
    print("Part 1: The product of the sizes is ", prod(len(comp) for comp in connected_components(graph)))
