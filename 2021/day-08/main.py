from typing import List


def count_1478(list: List[str]) -> int:

    count = 0

    for row in list:
        output_values = row.split(' | ')[1].split()
        for value in output_values:
            if len(value) in [2, 3, 4, 7]:
                count += 1

    return count


with open("2021/day-08/example.txt") as f:
    input = [str(line.strip()) for line in f]

    assert 26 == count_1478(input)


with open("2021/day-08/input.txt") as f:
    input = [str(line.strip()) for line in f]
    print("Part 1: The amount of 1478 is", count_1478(input))
    # print("Part 2: The sum of all outputs is", count_fish(input, 256))
