from typing import List, Tuple

def parse_input (lines: List[str]) -> List:
    mirrors = []
    mirror = []
    for i, line in enumerate(lines):
        if line == "":
            mirrors.append(mirror)
            mirror = []
        else:
            mirror.append(line)
    mirrors.append(mirror)

    return mirrors

def check_symmetry(mirror: List[str], pos: int):
    j = pos + 2
    pos -= 1
    while pos >= 0 and j < len(mirror):
        if mirror[pos] != mirror[j]:
            return False
        j += 1
        pos -= 1

    return True

def sum_all_mirrors(mirrors: List[List[str]]) -> int:
    rows = []
    columns = []

    for m, mirror in enumerate(mirrors):
        reflect_found = False
        for i, line in enumerate(mirror[:-1]):
            if line == mirror[i + 1]:
                if check_symmetry(mirror, i):
                    reflect_found = True
                    rows.append(i + 1)
                    break

        if reflect_found:
            continue

        mirror = list(map(list, zip(*mirror)))
        for i, line in enumerate(mirror[:-1]):
            if line == mirror[i + 1]:
                if check_symmetry(mirror, i):
                    columns.append(i + 1)
                    break

    return sum(columns) + 100 * sum(rows)

with open("2023/day-13/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    mirrors = parse_input(input_lines)

    assert 405 == sum_all_mirrors(mirrors)

with open("2023/day-13/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    mirrors = parse_input(input_lines)
    
    print("Part 1: The sum of all mirrors is ", sum_all_mirrors(mirrors))