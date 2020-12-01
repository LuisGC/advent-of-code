def report_repair(inputs):
    inputs.sort()

    for item in inputs:
        difference = 2020 - item
        if difference in inputs:
            return item * difference

    return false

with open("day-01/example.txt") as f:
    inputs = [int(line.strip()) for line in f]
    assert 514579 == report_repair(inputs)

with open("day-01/input.txt") as f:
    inputs = [int(line.strip()) for line in f]
    print ("Part 1:")
    print(report_repair(inputs))
