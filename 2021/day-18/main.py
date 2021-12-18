from typing import List


class SnailfishNumber:
    def __init__(self, value = None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        if isinstance(self.value, int):
            return str(self.value)
        return(f"[{str(self.left)},{str(self.right)}]")


def parse(number: List) -> SnailfishNumber:
    root = SnailfishNumber()
    if isinstance(number, int):
        root.value = number
        return root

    root.left = parse(number[0])
    root.left.parent = root
    root.right = parse(number[1])
    root.right.parent = root

    return root


def add(a: SnailfishNumber, b: SnailfishNumber) -> SnailfishNumber:
    root = SnailfishNumber()
    root.left = a
    root.left.parent = root
    root.right = b
    root.right.parent = root

    reduce(root)

    return root


def reduce(root: SnailfishNumber):

    # Do a DFS through the tree
    stack = [(root, 0)]

    done = True
    while len(stack) > 0:
        number, depth = stack.pop()

        if number == None:
            continue

        condition = (number.left == None and number.right == None) or (number.left.value != None and number.right.value != None)

        if depth >= 4 and number.value == None and condition:
            prev_node = number.left
            cur_node = number
            while cur_node != None and (cur_node.left == prev_node or cur_node.left == None):
                prev_node = cur_node
                cur_node = cur_node.parent

            if cur_node != None:
                cur_node = cur_node.left
                while cur_node.value == None:
                    if cur_node.right != None:
                        cur_node = cur_node.right
                    else:
                        cur_node = cur_node.left

                cur_node.value += number.left.value

            prev_node = number.right
            cur_node = number
            while cur_node != None and (cur_node.right == prev_node or cur_node.right == None):
                prev_node = cur_node
                cur_node = cur_node.parent

            if cur_node != None:
                cur_node = cur_node.right
                while cur_node.value == None:
                    if cur_node.left != None:
                        cur_node = cur_node.left
                    else:
                        cur_node = cur_node.right

                cur_node.value += number.right.value

            number.value = 0
            number.left = None
            number.right = None

            done = False
            break

        stack.append((number.right, depth + 1))
        stack.append((number.left, depth + 1))

    if not done:
        reduce(root)
        return

    stack = [root]
    while len(stack) > 0:
        number = stack.pop()
        if number == None:
            continue

        if number.value:
            assert not number.left and not number.right
            if number.value >= 10:
                number.left = SnailfishNumber(number.value//2)
                number.left.parent = number
                number.right = SnailfishNumber(number.value - (number.value//2))
                number.right.parent = number
                number.value = None

                done = False
                break

        stack.append(number.right)
        stack.append(number.left)

    if not done:
        reduce(root)


def add_and_reduce(snailfish_numbers: List) -> SnailfishNumber:
    root = parse(snailfish_numbers[0])

    for index in range (1, len(snailfish_numbers)):
        root = add(root, parse(snailfish_numbers[index]))
        # reduce(root)

    return root


def magnitude(number: SnailfishNumber) -> int:
    if isinstance(number.value, int):
        return number.value

    return 3 * magnitude(number.left) + 2 * magnitude(number.right)


def largest_magnitude(numbers: List) -> int:
    largest = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i == j:
                continue
            added_pair = add(parse(numbers[i]), parse(numbers[j]))
            current_magnitude = magnitude(added_pair)
            largest = max(largest, current_magnitude)
    return largest


snailfish_numbers = [eval("[[[[4,3],4],4],[7,[[8,4],9]]]"), eval("[1,1]")]
assert "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]" == str(add_and_reduce(snailfish_numbers))
snailfish_numbers = [eval("[1,1]"), eval("[2,2]"), eval("[3,3]"), eval("[4,4]")]
assert "[[[[1,1],[2,2]],[3,3]],[4,4]]" == str(add_and_reduce(snailfish_numbers))
snailfish_numbers = [eval("[1,1]"), eval("[2,2]"), eval("[3,3]"), eval("[4,4]"), eval("[5,5]")]
assert "[[[[3,0],[5,3]],[4,4]],[5,5]]" == str(add_and_reduce(snailfish_numbers))

with open("2021/day-18/example.txt") as f:
    snailfish_numbers = [eval(line.strip()) for line in f]
    result = add_and_reduce(snailfish_numbers)
    assert 3488 == magnitude(result)

with open("2021/day-18/homework.txt") as f:
    snailfish_numbers = [eval(line.strip()) for line in f]
    result = add_and_reduce(snailfish_numbers)
    assert 4140 == magnitude(result)
    assert 3993 == largest_magnitude(snailfish_numbers)

with open("2021/day-18/input.txt") as f:
    snailfish_numbers = [eval(line.strip()) for line in f]
    result = add_and_reduce(snailfish_numbers)
    print("Part 1: Magnitude of the result is:", magnitude(result))
    print("Part 2: Largest magnitude of any sum is:", largest_magnitude(snailfish_numbers))
