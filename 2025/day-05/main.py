def parse_input(input_lines):
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

with open("2025/day-05/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    ranges, ingredients = parse_input(input_lines)
    
    assert 3 == count_fresh(ranges, ingredients)

with open("2025/day-05/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    ranges, ingredients = parse_input(input_lines)

    print(f"Part 1: The amount of fresh ingredients is {count_fresh(ranges, ingredients)}")
#    print(f"Part 2: The amount of accessible rolls removing is {accessible_rolls(input_lines, removing=True)}")
