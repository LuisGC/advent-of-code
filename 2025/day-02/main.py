def invalid_ids(ranges: list[tuple[int, int]]) -> list[int]:
    invalid_ids = []

    for start, end in ranges:
        even_ids = [id_num for id_num in range(start, end + 1) if not len(str(id_num)) % 2]
        invalid_ids += [int(id_num) for id_num in even_ids if str(id_num).startswith(str(id_num)[len(str(id_num)) // 2:])]
    return invalid_ids

def get_ranges(input: list[str]) -> list[tuple[int, int]]:
    ranges = []
    for line in input.split(','):
        if line:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))
    return ranges

with open("2025/day-02/example.txt", encoding="utf-8") as f:
    ranges = get_ranges(f.readlines()[0])
    assert 1227775554 == sum(invalid_ids(ranges))

with open("2025/day-02/input.txt", encoding="utf-8") as f:
    ranges = get_ranges(f.readlines()[0])

    print(f"Part 1: The sum of all invalid ids is {sum(invalid_ids(ranges))}")
#    print(f"Part 2: The new password is {extract_password(input_lines, new_method=True)}")
