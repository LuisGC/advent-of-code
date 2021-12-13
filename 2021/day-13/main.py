from typing import List
from collections import defaultdict


class TransparentPaper:
    def __init__(self, dots: [int], fold_instructions: [(str, str)], max_x: int, max_y: int):
        self.paper = dots
        self.fold_instructions = fold_instructions
        self.max_x = max_x
        self.max_y = max_y


    def __str__(self):
        string = ''
        for line in self.paper:
            new_line = ''
            for dot in line:
                new_line += str(dot)

            string += new_line + '\n'

        for fold in self.fold_instructions:
            string += fold[0] + "=" + fold[1] + "\n"

        return string


def parse_input(input: List[str]) -> TransparentPaper:
    dots_array = []
    folds = []
    for line in input:
        if line == "\n" or line == "":
            pass
        elif line.startswith("fold"):
            folds.append(line.split(" ")[2].split("="))
        else:
            dots_array.append(line.split(','))

    max_x = max(int(dot[0]) for dot in dots_array)
    max_y = max(int(dot[1]) for dot in dots_array)

    paper = []

    for i in range(max_y + 1):
        paper.append([0] * (max_x + 1))

    for dot in dots_array:
        paper[int(dot[1])][int(dot[0])] = 1

    return TransparentPaper(paper, folds, max_x, max_y)


def count_dots(paper: List[int]) -> int:
    _sum = 0
    for i in range(len(paper)):
        for j in paper[i]:
            if j == 1:
                _sum += 1
    return _sum


def print_paper(paper: list) -> None:
    for i in range(len(paper)):
        for j in paper[i]:
            if j == 0:
                print(" ", end="")
            else:
                print("#", end="")
        print("")


def count_dots_after_fold(transparent_paper: TransparentPaper, folds: int) -> int:

    paper = transparent_paper.paper

    for fold in transparent_paper.fold_instructions[:folds]:
        axis = fold[0]
        coordinate = int(fold[1])
        if axis == "x":
            for line in paper:
                for i in range(transparent_paper.max_x - coordinate + 1):
                    try:
                        line[coordinate - i] |= line[coordinate + i]
                    except:
                        pass
                paper[paper.index(line)] = line[:coordinate]
        if axis == "y":
            for c in range(len(paper[0])):
                for i in range(transparent_paper.max_y - coordinate + 1):
                    try:
                        paper[coordinate - i][c] |= paper[coordinate + i][c]
                    except:
                        pass
            paper = paper[:coordinate]

    if (folds != 1):
        print_paper(paper)
    return count_dots(paper)


with open("2021/day-13/example.txt") as f:
    paper  = parse_input([line.strip() for line in f])
    assert 17 == count_dots_after_fold(paper, 1)

with open("2021/day-13/input.txt") as f:
    paper  = parse_input([line.strip() for line in f])
    print("Part 1: Total dots in 1 fold are : ", count_dots_after_fold(paper, 1))
    print("Part 2: The alphanumeric code is : ")
    count_dots_after_fold(paper, len(paper.fold_instructions))
