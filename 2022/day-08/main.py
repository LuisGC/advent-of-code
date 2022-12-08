import numpy as np

def count_visible_trees(trees: np.ndarray) -> int:
    
    visible = 2 * (trees.shape[0] + trees.shape[1]) - 4         # Perimeter trees

    for row in range(1, trees.shape[0] - 1):
        for col in range(1, trees.shape[1] - 1):
            if (np.all(trees[row,col] > trees[row,:col]) or     # left
                np.all(trees[row,col] > trees[row,col+1:]) or   # right
                np.all(trees[row,col] > trees[:row,col]) or     # up
                np.all(trees[row,col] > trees[row+1:,col])):    # down
                visible += 1

    return visible

def highest_scenic_score(trees: np.ndarray) -> int:
    highest = 0

    for row in range(1, trees.shape[0] - 1):
        for col in range(1, trees.shape[1] - 1):
            left = row - 1
            while left > 0 and trees[row,col] > trees[left, col]:
                left -= 1
            right = row + 1
            while right < trees.shape[0] - 1 and trees[row,col] > trees[right, col]:
                right += 1
            up = col - 1
            while up > 0 and trees[row, col] > trees[row, up]:
                up -= 1
            down = col + 1
            while down < trees.shape[1] - 1 and trees[row, col] > trees[row, down]:
                down += 1

            highest = max(highest, (row - left) * (right - row) * (col - up) * (down - col))

    return highest


with open("2022/day-08/example.txt", encoding="utf-8") as f:
    lines = [[int(x) for x in line.strip()] for line in f.readlines()]
    trees = np.array(lines)
    assert 21 == count_visible_trees(trees)
    assert 8 == highest_scenic_score(trees)

with open("2022/day-08/input.txt", encoding="utf-8") as f:
    lines = [[int(x) for x in line.strip()] for line in f.readlines()]
    trees = np.array(lines)
    print("Part 1: Count of visible trees is:", count_visible_trees(trees))
    print("Part 2: Highest scenic score is:", highest_scenic_score(trees))
