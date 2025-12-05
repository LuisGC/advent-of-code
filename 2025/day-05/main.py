def parse_input(input_lines) -> tuple[list[tuple[int, int]], list[int]]:
    ranges = []
    ingredients = []

    parsing_ranges = True

    for line in input_lines:
        if line == "":
            parsing_ranges = False
            continue

        if parsing_ranges:
            parts = line.split("-")
            ranges.append((int(parts[0]), int(parts[1])))
        else:
            ingredients.append(int(line))

    return ranges, ingredients

def count_fresh(ranges, ingredients) -> int:
    fresh_count = 0

    for ingredient in ingredients:
        is_fresh = False
        for start, end in ranges:
            if start <= ingredient <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_count += 1

    return fresh_count

def count_all_fresh(ranges) -> int:

    #removing overlapping ranges
    ranges.sort()

    i = 0
    while i < len(ranges) - 1:
        current_start, current_end = ranges[i]
        next_start, next_end = ranges[i + 1]

        if next_start <= current_end:
            ranges[i] = (current_start, max(current_end, next_end))
            ranges.pop(i + 1)
        else:
            i += 1
    
    return sum([end - start + 1 for start, end in ranges])


with open("2025/day-05/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    ranges, ingredients = parse_input(input_lines)

    assert 3 == count_fresh(ranges, ingredients)
    assert 14 == count_all_fresh(ranges)

with open("2025/day-05/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    ranges, ingredients = parse_input(input_lines)

    print(f"Part 1: The amount of fresh ingredients is {count_fresh(ranges, ingredients)}")
    print(f"Part 2: The total amount of fresh ingredients is {count_all_fresh(ranges)}")
