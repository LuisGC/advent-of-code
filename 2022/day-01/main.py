def max_calories(input_lines):

    max_calories = 0
    elf_calories = 0

    for x in input_lines:

        if x != '' and int(x) != 0:
            # print("X:", int(x))
            elf_calories += int(x)

        else:
            if elf_calories > max_calories:
                max_calories = elf_calories
            elf_calories = 0
        # print("current:" + str(elf_calories) + " Max: " + str(max_calories))
        
    return max_calories


def max_calories_by_3(input_lines):

    max_calories = [0,0,0]
    elf_calories = 0

    for x in input_lines:
        print("X:", x)

        if x == '':
            print("current:" + str(elf_calories) + " Max: " + str(max_calories))
            if elf_calories > max_calories[0]:
                max_calories[0] = elf_calories
                max_calories.sort()
            elf_calories = 0
        else:
            elf_calories += int(x)

    # This should not be necessary, but I am not processing the last blank line
    if elf_calories > max_calories[0]:
        max_calories[0] = elf_calories
        max_calories.sort()

    print("Max:", sum(max_calories))
    return sum(max_calories)


with open("2022/day-01/example.txt") as f:
    input_lines = [line.strip() for line in f]
    assert 24000 == max_calories(input_lines)
    assert 45000 == max_calories_by_3(input_lines)

with open("2022/day-01/input.txt") as f:
    input_lines = [line.strip() for line in f.readlines()]
    print("Part 1:", max_calories(input_lines))
    print("Part 2:", max_calories_by_3(input_lines))
