def calculate_gamma_epsilon(bits, length):

    gamma_rate = ["0"] * length
    epsilon_rate = ["1"] * length

    for x in range(0, len(bits)):
        if bits[x] > 0:
            gamma_rate[x] = "1"
            epsilon_rate[x] = "0"

    gamma_rate_str = ''.join(gamma_rate)
    epsilon_rate_str = ''.join(epsilon_rate)

    return int(gamma_rate_str,2) * int(epsilon_rate_str,2)


def calculate_power(inputs):

    length = len(inputs[0])
    commonbits = [0] * length

    for line in inputs:
        for x in range(0, length):
            oldvalue = commonbits[x]

            if line[x:x+1] == "1":
                commonbits[x] = oldvalue + 1
            else:
                commonbits[x] = oldvalue - 1

    power_consumption = calculate_gamma_epsilon(commonbits, length)

    return power_consumption


def calculate_life_support_rating(inputs):

    length = len(inputs[0])

    oxygen_array = []
    co2_array = []
    oxygen_done = False
    c02_done = False

    for i in range(length):
        values_o = [j[i] for j in oxygen_array or inputs]
        values_c = [j[i] for j in co2_array or inputs]

        oxygen_done = len(oxygen_array) == 1
        c02_done = len(co2_array) == 1

        if values_o.count("0") > values_o.count("1") and not oxygen_done:
            oxygen_array = [(oxygen_array or inputs)[v] for v in range(len(values_o)) if values_o[v] == "0"]
        elif not oxygen_done:
            oxygen_array = [(oxygen_array or inputs)[v] for v in range(len(values_o)) if values_o[v] == "1"]

        if values_c.count("0") > values_c.count("1") and not c02_done:
            co2_array = [(co2_array or inputs)[v] for v in range(len(values_c)) if values_c[v] == "1"]
        elif not c02_done:
            co2_array = [(co2_array or inputs)[v] for v in range(len(values_c)) if values_c[v] == "0"]

    oxygen = int(oxygen_array[0], 2)
    co2 = int(co2_array[0], 2)

    return oxygen * co2


with open("2021/day-03/example.txt") as f:
    inputs = [str(line.strip()) for line in f]
    assert 198 == calculate_power(inputs)
    assert 230 == calculate_life_support_rating(inputs)

with open("2021/day-03/input.txt") as f:
    inputs = [str(line.strip()) for line in f]
    print("Part 1:", calculate_power(inputs))
    print("Part 2:", calculate_life_support_rating(inputs))
