from collections import defaultdict


def recitate(initial_numbers, times):
    spoken = defaultdict(list)
    prev = -1

    for x in range(times):
        if x < len(initial_numbers):
            # one of the initial numbers
            spoken[initial_numbers[x]].append(x)
            prev = initial_numbers[x]
            continue

        if len(spoken[prev]) == 1:
            # this is a new number
            spoken[0].append(x)
            prev = 0
        else:
            # this number is not new
            d = spoken[prev][-1] - spoken[prev][-2]
            spoken[d].append(x)
            prev = d

    return prev


with open("day-15/example.txt") as f:
    input_numbers = f.read().strip().split(",")
    numbers = [int(numeric_string) for numeric_string in input_numbers]
    assert 436 == recitate(numbers, 2020)
    assert 175594 == recitate(numbers, 30000000)


with open("day-15/input.txt") as f:
    input_numbers = f.read().strip().split(",")
    numbers = [int(numeric_string) for numeric_string in input_numbers]
    print("Part 1: The 2020th recitated number is",
          recitate(numbers, 2020))
    print("Part 2: The 30000000th recitated number is",
          recitate(numbers, 30000000))
