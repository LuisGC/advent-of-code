def report_repair_2(inputs, total):
    inputs.sort()

    for item in inputs:
        difference = total - item
        if difference in inputs:
            return item * difference

    return 0


with open("2020/day-01/example.txt") as f:
    inputs = [int(line.strip()) for line in f]
    assert 514579 == report_repair_2(inputs, 2020)


with open("2020/day-01/input.txt") as f:
    inputs = [int(line.strip()) for line in f]
    print("Part 1:", report_repair_2(inputs, 2020))


def report_repair_3(inputs, total):
    inputs.sort()

    for item in inputs:
        difference = total - item

        repair_rest = report_repair_2(inputs, difference)
        if repair_rest != 0:
            return item * repair_rest

    return 0


with open("2020/day-01/example.txt") as f:
    inputs = [int(line.strip()) for line in f]
    assert 241861950 == report_repair_3(inputs, 2020)


with open("2020/day-01/input.txt") as f:
    inputs = [int(line.strip()) for line in f]
    print("Part 2:", report_repair_3(inputs, 2020))
