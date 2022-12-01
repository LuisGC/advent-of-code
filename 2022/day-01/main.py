def max_calories(input_lines):

    max_calories = 0
    elf_calories = 0

    for x in input_lines:

        if x != '' and int(x) != 0:
            # print("X:", int(x))
            elf_calories += int(x)

            if elf_calories > max_calories:
                max_calories = elf_calories
        else:
            elf_calories = 0
        # print("current:" + str(elf_calories) + " Max: " + str(max_calories))
        
    return max_calories


with open("2022/day-01/example.txt") as f:
    input_lines = [str(line.strip()) for line in f]
    assert 24000 == max_calories(input_lines)

with open("2022/day-01/input.txt") as f:
    input_lines = [str(line.strip()) for line in f]
    print("Part 1:", max_calories(input_lines))
