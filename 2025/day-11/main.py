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

    def dfs(node: str):
        nonlocal paths
        if node == end:
            paths += 1
            return
        for neighbor in graph.get(node, []):
            dfs(neighbor)
    
    dfs(start)
    return paths

with open("2025/day-11/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    graph = parse_input(input_lines)

    assert 5 == paths_between_nodes(graph, 'you', 'out')

with open("2025/day-11/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    graph = parse_input(input_lines)

    print(f"Part 1: The fewest button presses for light is {paths_between_nodes(graph, 'you', 'out')}")
