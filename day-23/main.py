from typing import List
from collections import deque


def rotate_until(cups: List[int], target_value: int) -> List[int]:
    while True:
        cup = cups.popleft()
        cups.append(cup)
        if cup == target_value:
            break
    return cups


def play_crab_cups_deque(input: str, rounds: int) -> List[int]:

    cups = deque([int(c) for c in input])
    max_value = max(cups)
    min_value = min(cups)

    for _ in range(rounds):
        current = cups.popleft()
        cups.append(current)

        # Player picks up three cups after the current cups
        picked_up = [cups.popleft(), cups.popleft(), cups.popleft()]

        # Player selects the destination cup, by default the value minus one
        destination_value = current-1

        # if the default destination does not exist, we keep on searching
        while destination_value not in cups:
            destination_value -= 1
            if destination_value < min_value:
                destination_value = max_value

        # now we rotate the queue until destination appears
        cups = rotate_until(cups, destination_value)

        # then we place the picked up cups after the destination
        cups.extend(picked_up)

        # and finally we rotate to the cup after current
        cups = rotate_until(cups, current)

    return cups


def read_labels(cup_labels: List[int]) -> int:
    cup_labels = rotate_until(cup_labels, 1)
    return ''.join(str(i) for i in list(cup_labels)[:-1])


def play_crab_cups_dict(input: str,
                        rounds: int,
                        max_value: int) -> List[int]:
                        
    cups_with_successor = {}

    for x, label in enumerate(input):
        if x > 0:
            cups_with_successor[int(input[x-1])] = int(label)

    cups_with_successor[int(input[-1])] = 10

    for x in range(10, 10**6):
        cups_with_successor[x] = x+1

    cups_with_successor[10**6] = int(input[0])

    n = len(cups_with_successor)

    current = int(input[0])

    for _ in range(rounds):
        a = cups_with_successor[current]
        b = cups_with_successor[a]
        c = cups_with_successor[b]
        d = cups_with_successor[c]

        moving = [a, b, c]

        cups_with_successor[current] = d

        destination = ((current-2) % n) + 1

        while destination in moving:
            destination = ((destination-2) % n) + 1

        cups_with_successor[c] = cups_with_successor[destination]
        cups_with_successor[destination] = a
        current = cups_with_successor[current]

    return cups_with_successor[1], cups_with_successor[cups_with_successor[1]]


final_positions = play_crab_cups_deque("389125467", 10)
assert "92658374" == read_labels(final_positions)

final_positions = play_crab_cups_deque("389125467", 100)
assert "67384529" == read_labels(final_positions)

final_positions = play_crab_cups_deque("123487596", 100)
print("Part 1: The labels after 100 rounds are: ",
      read_labels(final_positions))

next, next_2 = play_crab_cups_dict("389125467", 10000000, 1000000)
print(next, next_2)
assert 934001 == next
assert 159792 == next_2
assert 149245887792 == next * next_2
next, next_2 = play_crab_cups_dict("123487596", 10000000, 1000000)
print("Part 2: The product of the next 2 labels after 10M rounds is: ",
      next * next_2)
