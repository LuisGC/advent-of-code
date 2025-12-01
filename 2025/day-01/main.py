def extract_password(input_lines: list[str]) -> int:
    password = 0
    position = 50
    
    for line in input_lines:
        if line:
            for i in range(int(line[1:])):
                position = (position + [-1, 1][line[0] == 'R']) % 100

            password += position == 0
    return password

with open("2025/day-01/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 3 == extract_password(input_lines)

with open("2025/day-01/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: The password is {extract_password(input_lines)}")
#    print(f"Part 2: Sum of all sim scores is {sim_score(input_lines)}")
