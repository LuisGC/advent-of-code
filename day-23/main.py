from typing import List
from collections import deque


def rotate_until(cups: List[int], target_value: int) -> List[int]:
    while True:
        cup = cups.popleft()
        cups.append(cup)
        if cup == target_value:
            break
    return cups


def play_crab_cups(input: str, rounds: int) -> List[int]:

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
    # we always finish with
    cup_labels = rotate_until(cup_labels, 1)
    return ''.join(str(i) for i in list(cup_labels)[:-1])


final_positions = play_crab_cups("389125467", 10)
assert "92658374" == read_labels(final_positions)

final_positions = play_crab_cups("389125467", 100)
assert "67384529" == read_labels(final_positions)

final_positions = play_crab_cups("123487596", 100)
print("Part 1: The labels after 100 rounds are: ",
      read_labels(final_positions))
