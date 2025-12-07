def count_splits(lines: list[list[str]]) -> int:
    beams = set([lines.pop(0).index("S")])
    total_splits = 0

    for line in lines:
        copy = beams.copy()

        for beam in copy:
            if line[beam] != '^':
                continue

            beams.remove(beam)
            beams.add(beam - 1)
            beams.add(beam + 1)
            total_splits += 1

    return total_splits

with open("2025/day-07/example.txt", encoding="utf-8") as f:
    input_lines = [list(line) for line in f.readlines()]

    assert 21 == count_splits(input_lines)

with open("2025/day-07/input.txt", encoding="utf-8") as f:
    input_lines = [list(line) for line in f.readlines()]

    print(f"Part 1: The total of splits is {count_splits(input_lines)}")
