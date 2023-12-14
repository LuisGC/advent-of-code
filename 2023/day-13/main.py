from typing import List

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

def similar_enough(reflect1: str, reflect2: str) -> bool:
    diff_count = 0
    for i, char in enumerate(reflect1):
        if char != reflect2[i]:
            diff_count += 1
        if diff_count > 1:
            return False
        
    return True


def check_symmetry(mirror: List[str], pos: int, with_smudges: bool=False):
    j = pos + 2
    pos -= 1
    while pos >= 0 and j < len(mirror):
        if with_smudges:
            if not similar_enough(mirror[pos], mirror[j]):
                return False
        else:
            if mirror[pos] != mirror[j]:
                return False
        j += 1
        pos -= 1

    return True

def sum_all_mirrors(mirrors: List[List[str]], with_smudges: bool = False) -> int:
    rows = []
    columns = []
    symetries = []

    for mirror in mirrors:
        reflect_found = False
        for i, line in enumerate(mirror[:-1]):
            if line == mirror[i + 1]:
                if check_symmetry(mirror, i):
                    reflect_found = True
                    rows.append(i + 1)
                    symetries.append(("row", i + 1))
                    break

        if reflect_found:
            continue

        mirror = list(map(list, zip(*mirror)))
        for i, line in enumerate(mirror[:-1]):
            if line == mirror[i + 1]:
                if check_symmetry(mirror, i):
                    columns.append(i + 1)
                    symetries.append(("col", i + 1))
                    break

    if with_smudges:
        rows = []
        columns = []

        for m, mirror in enumerate(mirrors):
            reflect_found = False
            for i, line in enumerate(mirror[:-1]):
                if line == mirror[i + 1] and (symetries[m][0] != "row" or symetries[m][1] != i + 1):
                    if  check_symmetry(mirror, i, with_smudges=True):
                        reflect_found = True
                        rows.append(i + 1)
                        break

            if reflect_found:
                continue

            mirror = list(map(list, zip(*mirror)))
            for i, line in enumerate(mirror[:-1]):
                if line == mirror[i + 1] and (symetries[m][0] != "col" or symetries[m][1] != i + 1):
                    if check_symmetry(mirror, i, with_smudges=True):
                        columns.append(i + 1)
                        break

            if reflect_found:
                continue

            mirror = list(map(list, zip(*mirror)))
            for i, line in enumerate(mirror[:-1]):
                if similar_enough(line, mirror[i + 1]) and (symetries[m][0] != "row" or symetries[m][1] != i + 1):
                    if check_symmetry(mirror, i, False):
                        rows.append(i + 1)
                        break

            if reflect_found:
                continue

            mirror = list(map(list, zip(*mirror)))
            for i, line in enumerate(mirror[:-1]):
                if similar_enough(line, mirror[i + 1]) and (symetries[m][0] != "col" or symetries[m][1] != i + 1):
                    if check_symmetry(mirror, i, False):
                        columns.append(i + 1)
                        break

    return sum(columns) + 100 * sum(rows)

with open("2023/day-13/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    mirrors = parse_input(input_lines)

    assert 405 == sum_all_mirrors(mirrors)
    assert 400 == sum_all_mirrors(mirrors, with_smudges=True)

with open("2023/day-13/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    mirrors = parse_input(input_lines)
    
    print("Part 1: The sum of all mirrors is ", sum_all_mirrors(mirrors))
    print("Part 2: The sum with smudges is ", sum_all_mirrors(mirrors, with_smudges=True))