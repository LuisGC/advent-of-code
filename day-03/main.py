def traverse(forest, delta_x, delta_y) -> int:

    x = 0
    y = 0
    num_trees = 0
    width = len(forest[0]) - 1

    while y < len(forest):
        if forest[y][x] == "#":
            num_trees += 1

        x, y = (x + delta_x) % width, y + delta_y

    return num_trees


with open("day-03/example.txt") as f:
    forest = f.readlines()
    assert 7 == traverse(forest, 3, 1)


with open("day-03/input.txt") as f:
    forest = f.readlines()
    print("Part 1, Number of trees:", traverse(forest, 3, 1))

# PART 2

with open("day-03/example.txt") as f:
    forest = f.readlines()
    assert 2 == traverse(forest, 1, 1)
    assert 7 == traverse(forest, 3, 1)
    assert 3 == traverse(forest, 5, 1)
    assert 4 == traverse(forest, 7, 1)
    assert 2 == traverse(forest, 1, 2)

with open("day-03/input.txt") as f:
    forest = f.readlines()
    print("Part 2")
    traverse_1 = traverse(forest, 1, 1)
    traverse_2 = traverse(forest, 3, 1)
    traverse_3 = traverse(forest, 5, 1)
    traverse_4 = traverse(forest, 7, 1)
    traverse_5 = traverse(forest, 1, 2)

    print("Number of trees with 1,1:", traverse_1)
    print("Number of trees with 3,1:", traverse_2)
    print("Number of trees with 5,1:", traverse_3)
    print("Number of trees with 7,1:", traverse_4)
    print("Number of trees with 1,2:", traverse_5)
    print("The product is",
          traverse_1 * traverse_2 * traverse_3 * traverse_4 * traverse_5)
