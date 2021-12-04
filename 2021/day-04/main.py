from __future__ import annotations
from typing import NamedTuple, Sequence


class BingoCard (NamedTuple):
    numbers: Sequence[int]


def card_score(draws: Sequence[int], card: BingoCard) -> int:

    drawn = [False] * 25
    draw_set = set(draws)

    for i, board_num in enumerate(card.numbers):
        if board_num in draw_set:
            drawn[i] = True

    bingo = False

    for i in range(5):
        if all([drawn[col] for col in range(5*i, 5*i+5)]):
            bingo = True

        if all([drawn[row] for row in range(i, 25, 5)]):
            bingo = True

    if not bingo:
        return 0

    s = sum([card.numbers[i] for i, is_drawn in enumerate(drawn) if not is_drawn])
    return s * draws[len(draws)-1]


def play_bingo (draws, cards):

    for i in range(len(draws)):
        for card in cards:
            score = card_score(draws[:i], card)
            if score != 0:
                return score

    return 0


def parse_input (input):

    chunks = "\n".join(input).split("\n\n")

    draws = tuple(map(int, chunks[0].split(",")))
    cards = [BingoCard(tuple(int(i) for i in card.split())) for card in chunks[1:]]

    return draws, cards


with open("2021/day-04/example.txt") as f:
    input = [str(line.strip()) for line in f]
    draws, cards = parse_input(input)

    assert 4512 == play_bingo(draws,cards)


with open("2021/day-04/input.txt") as f:
    input = [str(line.strip()) for line in f]
    draws, cards = parse_input(input)
    print("Part 1: Bingo winner score is", play_bingo(draws,cards))
#    print("Part 2: distance * depth with aim is", run_commands_aim(commands))
