from functools import cmp_to_key

def sum_middle_pages(lines: list, with_fix: bool = False) -> int:

    def compare(x, y):
        if (x,y) in dd: return -1
        if (y, x) in dd: return 1
        return 0
    
    result = 0
    dict = {}
    dd = set()

    for line in lines:
        if '|' in line:
            left, right = line.replace("\n", "").split("|")
            if left in dict:
                dict[left].append(right)
            else:
                dict[left] = [right]
            dd.add((left, right))
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
            if not with_fix and good:
                result += int(pages[len(pages)//2])
            elif not good and with_fix:
                pages.sort(key=cmp_to_key(compare))
                result += int(pages[len(pages)//2])

    return result

with open("2024/day-05/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 143 == sum_middle_pages(input_lines)
    assert 123 == sum_middle_pages(input_lines, with_fix=True)

with open("2024/day-05/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: Sum of middle page numbers is {sum_middle_pages(input_lines)}")
    print(f"Part 2: Sum of middle page numbers with fix is {sum_middle_pages(input_lines, with_fix=True)}")
