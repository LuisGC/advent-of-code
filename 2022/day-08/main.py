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

with open("2022/day-08/example.txt", encoding="utf-8") as f:
    trees = [[int(x) for x in line.strip()] for line in f.readlines()]
    assert 21 == count_visible_trees(np.array(trees))

with open("2022/day-08/input.txt", encoding="utf-8") as f:
    trees = [[int(x) for x in line.strip()] for line in f.readlines()]
    print("Part 1: Count of visible trees is:", count_visible_trees(np.array(trees)))
