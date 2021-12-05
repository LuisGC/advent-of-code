

def parse_input(input):
    return [[(line.split()[0]).split(','), (line.split()[2]).split(',')] for line in input]


def overlaping_points(diagram_list: list) -> int:

    diagram = {}

    for line in diagram_list:
        if line[0][0] == line[1][0] or line[0][1] == line[1][1]:
            low_x = min(int(line[0][0]), int(line[1][0]))
            high_x = max(int(line[0][0]), int(line[1][0]))
            low_y = min(int(line[0][1]), int(line[1][1]))
            high_y = max(int(line[0][1]), int(line[1][1]))
            for x in range(low_x, high_x+1):
                for y in range(low_y, high_y+1):
                    if x in diagram:
                        if y in diagram[x]:
                            diagram[x][y] = diagram[x][y] + 1
                        else:
                            diagram[x][y] = 1
                    else:
                        diagram[x] = {y: 1}

    overlaping_points = 0

    for x in diagram:
        for y in diagram[x]:
            if diagram[x][y] >= 2:
                overlaping_points += 1

    return overlaping_points


with open("2021/day-05/example.txt") as f:
    input = [str(line.strip()) for line in f]
    diagram = parse_input(input)

    assert 5 == overlaping_points(diagram)


with open("2021/day-05/input.txt") as f:
    input = [str(line.strip()) for line in f]
    diagram = parse_input(input)
    print("Part 1: The amount of overlaping points is", overlaping_points(diagram))
#    print("Part 2: Bingo loser score is", play_to_lose(draws, cards))
