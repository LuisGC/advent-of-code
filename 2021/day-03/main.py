def calculate_gamma_epsilon(bits, length):

    gamma_rate = ["0"] * length
    epsilon_rate = ["1"] * length

    for x in range(0, len(bits)):
        if bits[x] > 0:
            gamma_rate[x] = "1"
            epsilon_rate[x] = "0"

    gamma_rate_str = ''.join(gamma_rate)
    epsilon_rate_str = ''.join(epsilon_rate)

    print(gamma_rate_str, type(gamma_rate_str))
    print(epsilon_rate_str)

    print(int(gamma_rate_str,2))

    return int(gamma_rate_str,2) * int(epsilon_rate_str,2)


def calculate_power(inputs):

    length = len(str(inputs[1]))
    print("first line:",inputs[1])
    print(length)

    commonbits = [0] * length

    for line in inputs:
        print(line)
        for x in range(0, length):
            oldvalue = commonbits[x]

            if line[x:x+1] == "1":
                commonbits[x] = oldvalue + 1
            else:
                commonbits[x] = oldvalue - 1

    print("common bits:",commonbits)

    power_consumption = calculate_gamma_epsilon(commonbits, length)

    return power_consumption


with open("2021/day-03/example.txt") as f:
    inputs = [str(line.strip()) for line in f]
    assert 198 == calculate_power(inputs)

with open("2021/day-03/input.txt") as f:
    inputs = [str(line.strip()) for line in f]
    print("Part 1:", calculate_power(inputs))
