def count_splits(lines: list[list[str]], initial_beam: int) -> int:
    beams = set([initial_beam])
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

def count_quantum_splits(lines: list[list[str]], initial_beam: int) -> int:
    beams = {initial_beam: 1}

    for line in lines:
        copy = beams.copy()

        for beam in copy.keys():
            if line[beam] != '^':
                continue

            count = beams[beam]

            for split in [beam - 1, beam + 1]:
                if split in beams:
                    beams[split] += count
                else:
                    beams[split] = count
            beams.pop(beam)

    return sum(beams.values())


with open("2025/day-07/example.txt", encoding="utf-8") as f:
    input_lines = [list(line) for line in f.readlines()]
    initial_beam = input_lines.pop(0).index("S")

    assert 21 == count_splits(input_lines, initial_beam)
    assert 40 == count_quantum_splits(input_lines, initial_beam)

with open("2025/day-07/input.txt", encoding="utf-8") as f:
    input_lines = [list(line) for line in f.readlines()]
    initial_beam = input_lines.pop(0).index("S")

    print(f"Part 1: The total of splits is {count_splits(input_lines, initial_beam)}")
    print(f"Part 2: The total of quantum splits is {count_quantum_splits(input_lines, initial_beam)}")
