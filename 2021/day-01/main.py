def count_increase(inputs):

    count = 0

    for x in range(0, len(inputs)-1):
        if inputs[x] < inputs[x+1]:
            count = count + 1

    return count


with open("2021/day-01/example.txt") as f:
    inputs = [int(line.strip()) for line in f]
    print(inputs)
    assert 7 == 0 + count_increase(inputs)

with open("2021/day-01/input.txt") as f:
    inputs = [int(line.strip()) for line in f]
    print("Part 1:", 0 + count_increase(inputs))
