def count_increase(inputs):

    count = 0

    for x in range(0, len(inputs)-1):
        count += (inputs[x] < inputs[x+1])

    return count


with open("2021/day-01/example.txt", encoding="utf-8") as f:
    inputs = [int(line.strip()) for line in f]
    assert 7 == count_increase(inputs)

with open("2021/day-01/input.txt", encoding="utf-8") as f:
    inputs = [int(line.strip()) for line in f]
    print("Part 1:", count_increase(inputs))


def count_increase_window(inputs):

    count = 0

    for x in range(0, len(inputs)-3):
        count += inputs[x] + inputs[x+1] + inputs[x+2] < inputs[x+1] + inputs[x+2] + inputs[x+3]

    return count


with open("2021/day-01/example.txt", encoding="utf-8") as f:
    inputs = [int(line.strip()) for line in f]
    assert 5 == count_increase_window(inputs)

with open("2021/day-01/input.txt", encoding="utf-8") as f:
    inputs = [int(line.strip()) for line in f]
    print("Part 2:", count_increase_window(inputs))
