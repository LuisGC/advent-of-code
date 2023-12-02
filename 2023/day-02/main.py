def verify_game(line: str, max_red: int, max_green: int, max_blue:int) -> bool:
    games = line.split(": ")[1].split("; ")
    for game in games:
        draws = game.split(", ")
        for draw in draws:
            amount, color = draw.split(" ")
            if color == "red" and int(amount) > max_red:
                return False
            if color == "green" and int(amount) > max_green:
                return False
            if color == "blue" and int(amount) > max_blue:
                return False

    return True

def min_possible_cubes_power(line: str) -> int:
    games = line.split(": ")[1].split("; ")
    min_red = min_green = min_blue = 0
    for game in games:
        draws = game.split(", ")
        for draw in draws:
            amount, color = draw.split(" ")
            if color == "red" and int(amount) > min_red:
                min_red = int(amount)
            if color == "green" and int(amount) > min_green:
                min_green = int(amount)
            if color == "blue" and int(amount) > min_blue:
                min_blue = int(amount)

    return min_red * min_green * min_blue

with open("2023/day-02/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = total_power = 0
    for i,line in enumerate(input_lines):
        if verify_game(line, 12, 13, 14):
            total += i+1
        total_power += min_possible_cubes_power(line)

    assert 8 == total
    assert 2286 == total_power

with open("2023/day-02/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    total = total_power = 0
    for i,line in enumerate(input_lines):
        if verify_game(line, 12, 13, 14):
            total += i+1
        total_power += min_possible_cubes_power(line)

    print("Part 1: Sum of all valid games is ", total)
    print("Part 2: Sum of all powers of required sets is ", total_power)
