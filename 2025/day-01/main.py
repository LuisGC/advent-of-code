def extract_password(input_lines: list[str], new_method: bool = False) -> int:
    password, new_password = 0, 0
    position = 50
    
    for line in input_lines:
        if line:
            for i in range(int(line[1:])):
                position = (position + [-1, 1][line[0] == 'R']) % 100
                new_password += position == 0
            password += position == 0
    
    if new_method:
        return new_password
    else:
        return password

with open("2025/day-01/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    assert 3 == extract_password(input_lines)

with open("2025/day-01/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: The password is {extract_password(input_lines)}")
    print(f"Part 2: The new password is {extract_password(input_lines, new_method=True)}")
