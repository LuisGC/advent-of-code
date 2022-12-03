def parse_input(input):
    return [[(line.split()[0]).split(','), (line.split()[2]).split(',')] for line in input]


def update_diagram(diagram: dict, x: int, y: int) -> dict:
    if x in diagram:
        if y in diagram[x]:
            diagram[x][y] = diagram[x][y] + 1
        else:
            diagram[x][y] = 1
    else:
        diagram[x] = {y: 1}


def overlaping_points(diagram_list: list, diagonal_counts: bool) -> int:

    diagram = {}

    for line in diagram_list:

        horizontal = line[0][0] == line[1][0]
        vertical = line[0][1] == line[1][1]
        diagonal_positive = line[0][0] == line[0][1] and line[1][0] == line[1][1]
        diagonal_negative = line[0][0] == line[1][1] and line[1][0] == line[0][1]

        low_x = min(int(line[0][0]), int(line[1][0]))
        high_x = max(int(line[0][0]), int(line[1][0]))
        low_y = min(int(line[0][1]), int(line[1][1]))
        high_y = max(int(line[0][1]), int(line[1][1]))

        if horizontal or vertical:
            for x in range(low_x, high_x+1):
                for y in range(low_y, high_y+1):
                    update_diagram(diagram, x, y)

        elif diagonal_counts and (diagonal_positive or diagonal_negative):
            for x in range(low_x, high_x+1):
                if diagonal_positive:
                    y = x
                else:
                    y = -x + int(line[0][0]) + int(line[0][1])

                update_diagram(diagram, x, y)

        elif diagonal_counts:
            x_start = int(line[0][0])
            x_end = int(line[1][0])
            y_start = int(line[0][1])
            y_end = int(line[1][1])

            m = int((y_end-y_start)/(x_end-x_start))

            for x in range(low_x, high_x+1):
                y = m*(x - x_start) + y_start
                update_diagram(diagram, x, y)

    overlaping_points = 0

    for x in diagram:
        for y in diagram[x]:
            if diagram[x][y] >= 2:
                overlaping_points += 1

    return overlaping_points


with open("2021/day-05/example.txt", encoding="utf-8") as f:
    input = [str(line.strip()) for line in f]
    diagram = parse_input(input)

    assert 5 == overlaping_points(diagram, False)
    assert 12 == overlaping_points(diagram, True)


with open("2021/day-05/input.txt", encoding="utf-8") as f:
    input = [str(line.strip()) for line in f]
    diagram = parse_input(input)
    print("Part 1: The amount of overlaping points is", overlaping_points(diagram, False))
    print("Part 2: The amount of overlaping points with diagonals is", overlaping_points(diagram, True))
