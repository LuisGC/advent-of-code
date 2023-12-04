import re
from typing import Tuple

def calculate_score(cards: list) -> Tuple[int, int]:
    old_score = 0
    cards_won = []
    for index, card in enumerate(cards):
        _, winning, playing = re.split(r':\s+|\s+\|\s+', card)
        winning = set(int(w) for w in re.split(r'\s+', winning))
        playing = set(int(y) for y in re.split(r'\s+', playing))
        common = winning.intersection(playing)
        old_score += 2 ** (len(common) - 1) if len(common) > 0 else 0
        try:
            cards_won[index] += 1
        except IndexError:
            cards_won.append(1)
        for _ in range(cards_won[index]):
            for i in range(len(common)):
                try:
                    cards_won[index + 1 + i] += 1
                except IndexError:
                    cards_won.append(1)

    return old_score, sum(cards_won)


with open("2023/day-04/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    score, cards_won = calculate_score(input_lines)
    assert 13 == score
    assert 30 == cards_won

with open("2023/day-04/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    score, cards_won = calculate_score(input_lines)
    print("Part 1: Score of all cards is ", score)
    print("Part 2: Number of cards won is ", cards_won)
