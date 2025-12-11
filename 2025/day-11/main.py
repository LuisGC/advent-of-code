from functools import lru_cache

def parse_input(lines: list[str]) -> dict[str, list[str]]:
    graph = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        left, right = line.split(":")
        node = left.strip()
        neighbors = right.strip().split()
        graph[node] = neighbors

    return graph

def paths_between_nodes(graph: dict[str, list[str]], start: str, end: str) -> int:
    paths = 0

    # DFS to count paths
    def dfs(node: str):
        nonlocal paths
        if node == end:
            paths += 1
            return
        for neighbor in graph.get(node, []):
            dfs(neighbor)
    
    dfs(start)
    return paths

def paths_with_stages(graph: dict[str, list[str]], start: str, end: str, stages: list[str]) -> int:
    
    def count_paths(graph: dict[str, list[str]], start: str, end: str) -> int:

        # DFS with memoization to count paths
        @lru_cache(None)
        def dfs(node: str) -> int:
            if node == end:
                return 1
            return sum(dfs(neighbor) for neighbor in graph.get(node, []))

        return dfs(start)                       

    paths = (
        count_paths(graph, start, stages[0]) * count_paths(graph, stages[0], stages[1]) * count_paths(graph, stages[1], end)
    + count_paths(graph, start, stages[1]) * count_paths(graph, stages[1], stages[0]) * count_paths(graph, stages[0], end)
    )
    
    return paths


with open("2025/day-11/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    graph = parse_input(input_lines)

    assert 5 == paths_between_nodes(graph, 'you', 'out')

with open("2025/day-11/example-2.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    graph = parse_input(input_lines)

    assert 2 == paths_with_stages(graph, 'svr', 'out', ['dac', 'fft'])

with open("2025/day-11/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    graph = parse_input(input_lines)

    print(f"Part 1: The amount of different paths is {paths_between_nodes(graph, 'you', 'out')}")
    print(f"Part 2: The amount of different paths is {paths_with_stages(graph, 'svr', 'out', ['dac', 'fft'])}")
