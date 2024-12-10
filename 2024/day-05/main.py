def sum_middle_pages(lines: list) -> int:
    result = 0
    dict = {}

    for line in lines:
        if '|' in line:
            left, right = line.replace("\n", "").split("|")
            if left in dict:
                dict[left].append(right)
            else:
                dict[left] = [right]
        if ',' in line:
            pages = line.replace("\n", "").split(",")
            done = set()
            good = True
            for page in pages:
                if page in dict:
                    for after in dict[page]:
                        if after in done:
                            good = False
                done.add(page)
            if good:
                result += int(pages[len(pages)//2])

    return result

with open("2024/day-05/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 143 == sum_middle_pages(input_lines)

with open("2024/day-05/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: Sum of middle page numbers is {sum_middle_pages(input_lines)}")
#    print(f"Part 2: X-MAS found times is {count_X_MAS(input_lines)}")
