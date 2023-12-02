RED = {"name": "red", "max": 12}
GREEN = {"name": "green", "max": 13}
BLUE = {"name": "blue", "max": 14}

def verify_game(line: str) -> bool:
    games = line.split(": ")[1].split("; ")
    for game in games:
        draws = game.split(", ")
        for draw in draws:
            amount, color = draw.split(" ")
            if color == RED["name"] and int(amount) > RED["max"]:
                return False
            if color == GREEN["name"] and int(amount) > GREEN["max"]:
                return False
            if color == BLUE["name"] and int(amount) > BLUE["max"]:
                return False

    return True

def min_possible_cubes_power(line: str) -> int:
    games = line.split(": ")[1].split("; ")
    min_red = min_green = min_blue = 0
    for game in games:
        draws = game.split(", ")
        for draw in draws:
            amount, color = draw.split(" ")
            if color == RED["name"] and int(amount) > min_red:
                min_red = int(amount)
            if color == GREEN["name"] and int(amount) > min_green:
                min_green = int(amount)
            if color == BLUE["name"] and int(amount) > min_blue:
                min_blue = int(amount)

    return min_red * min_green * min_blue

with open("2023/day-02/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = total_power = 0
    for i,line in enumerate(input_lines):
        if verify_game(line):
            total += i+1
        total_power += min_possible_cubes_power(line)

    assert 8 == total
    assert 2286 == total_power

with open("2023/day-02/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = total_power = 0
    for i,line in enumerate(input_lines):
        if verify_game(line):
            total += i+1
        total_power += min_possible_cubes_power(line)

    print("Part 1: Sum of all valid games is ", total)
    print("Part 2: Sum of all powers of required sets is ", total_power)
