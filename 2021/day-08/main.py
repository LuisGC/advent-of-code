from typing import List


def count_1478(list: List[str]) -> int:

    count = 0

    for row in list:
        output_values = row.split(' | ')[1].split(" ")
        for value in output_values:
            if len(value) in [2, 3, 4, 7]:
                count += 1

    return count


def obtain_possibilities(nums: List[str]) -> List[str]:

    solving_order = [2, 3, 4, 7]
    possibilities = []

    for item in solving_order:
        for num in nums:
            digit_length = len(num)
            if item == digit_length:

                if digit_length == 2:       # 1
                    possibilities.append(['', '', num[0], '', '', num[1], ''])
                    possibilities.append(['', '', num[1], '', '', num[0], ''])

                elif digit_length == 3:     # 7
                    for pos in possibilities:
                        for digit in num:
                            if digit not in pos:
                                pos[0] = digit

                elif digit_length == 4:     # 4
                    new_possibilities = []
                    for pos in possibilities:
                        new_segments = []
                        for digit in num:
                            if digit not in pos:
                                new_segments.append(digit)
                        new_possibilities.append([pos[0], new_segments[0], pos[2], new_segments[1], '', pos[5], ''])
                        new_possibilities.append([pos[0], new_segments[1], pos[2], new_segments[0], '', pos[5], ''])
                    possibilities = new_possibilities

                elif digit_length == 7:     # 8
                    new_possibilities = []
                    for pos in possibilities:
                        new_segments = []
                        for digit in num:
                            if digit not in pos:
                                new_segments.append(digit)
                        new_possibilities.append([pos[0], pos[1], pos[2], pos[3], new_segments[0], pos[5], new_segments[1]])
                        new_possibilities.append([pos[0], pos[1], pos[2], pos[3], new_segments[1], pos[5], new_segments[0]])
                    possibilities = new_possibilities

    return possibilities


def obtain_solution(nums: List[str], possibilities: List[str]) -> List[str]:

    for pos in possibilities:
        possible_solution = [""] * 10

        for num in nums:
            if len(num) == 2:
                possible_solution[1] = num
            elif len(num) == 3:
                possible_solution[7] = num
            elif len(num) == 4:
                possible_solution[4] = num
            elif len(num) == 7:
                possible_solution[8] = num
            elif len(num) == 6:                                 # 0, 6 or 9
                if pos[3] not in num:                           # 0
                    possible_solution[0] = num
                elif pos[2] not in num:                         # 6
                    possible_solution[6] = num
                elif pos[4] not in num:                         # 9
                    possible_solution[9] = num
            elif len(num) == 5:                                 # 2, 3 or 5
                if pos[5] not in num:                           # 2
                    possible_solution[2] = num
                elif pos[1] not in num and pos[4] not in num:   # 3
                    possible_solution[3] = num
                elif pos[2] not in num:                         # 5
                    possible_solution[5] = num

        if "" not in possible_solution:
            return possible_solution


def count_output(output: List[str], solution: List[str]) -> int:
    output_decoded = ''
    for number in output:
        for i in range(len(solution)):
            if sorted(number) == sorted(solution[i]):
                output_decoded += str(i)

    return int(output_decoded)


def sum_all_outputs(list: List[str]) -> int:
    sum = 0

    for row in list:
        parts = row.split(' | ')
        nums = ["".join(x) for x in parts[0].split(" ")]
        output = ["".join(x) for x in parts[1].split(" ")]

        possibilities = obtain_possibilities(nums)

        final_solution = obtain_solution(nums, possibilities)

        sum += count_output(output, final_solution)

    return sum


with open("2021/day-08/example.txt", encoding="utf-8") as f:
    input = [str(line.strip()) for line in f]

    assert 26 == count_1478(input)
    assert 61229 == sum_all_outputs(input)


with open("2021/day-08/input.txt", encoding="utf-8") as f:
    input = [str(line.strip()) for line in f]
    print("Part 1: The amount of 1478 is", count_1478(input))
    print("Part 2: The sum of all outputs is", sum_all_outputs(input))
