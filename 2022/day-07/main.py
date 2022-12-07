from typing import List

def parse_input(lines: List) -> dict:
    filesystem = {}
    path = ['/']

    for line in lines:
        if "$" in line:
            if "cd" in line:
                if "/" in line:
                    path = ["/"]
                elif ".." in line:
                    path.pop()
                else:
                    path.append(line[5:])
        else:
            if "dir" not in line:
                for i in range(len(path)):
                    dir = ",".join(path[:i+1])
                    filesystem[dir] = (filesystem.get(dir) or 0) + int(line.split()[0])

    # print("Filesystem:", filesystem)
    return filesystem

def count_files_under_threshold(filesystem: dict, threshold: int=100000) -> int:
    count = 0
    for file in filesystem.values():
        if file <= threshold:
            count += file

    return count

def find_optimal_dir_size(filesystem: dict) -> int:
    to_be_deleted = 30000000 - (70000000 - filesystem.get("/"))
    for dir_size in list(sorted(filesystem.values())):
        if dir_size >= to_be_deleted:
            return dir_size
            break


with open("2022/day-07/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    filesystem = parse_input(input_lines)

    assert 95437 == count_files_under_threshold(filesystem)
    assert 24933642 == find_optimal_dir_size(filesystem)

with open("2022/day-07/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    filesystem = parse_input(input_lines)

    print("Part 1: Count of files under threshold is:", count_files_under_threshold(filesystem))
    print("Part 2: Optimal dir size to be removed is ", find_optimal_dir_size(filesystem))
