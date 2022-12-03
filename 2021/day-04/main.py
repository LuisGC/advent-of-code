from typing import NamedTuple, Sequence, Set


class BingoCard (NamedTuple):
    numbers: Sequence[int]


def card_score(draws: Sequence[int], card: BingoCard) -> int:

    drawn = [False] * 25
    draw_set = set(draws)

    for i, card_num in enumerate(card.numbers):
        if card_num in draw_set:
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


def play_to_win(draws: Sequence[int], cards: Sequence[BingoCard]) -> int:

    for i in range(len(draws)):
        for card in cards:
            score = card_score(draws[:i], card)
            if score != 0:
                return score

    return 0


def play_to_lose(draws: Sequence[int], cards: Sequence[BingoCard]) -> int:

    winners: Set[int] = set()
    for i in range(len(draws)):
        for card_num, card in enumerate(cards):
            score = card_score(draws[:i], card)
            if score != 0 and card_num not in winners:
                if len(winners) == len(cards) - 1:
                    return score
                winners.add(card_num)

    return 0


def parse_input(input):

    chunks = "\n".join(input).split("\n\n")
    draws = tuple(map(int, chunks[0].split(",")))
    cards = [BingoCard(tuple(int(i) for i in card.split())) for card in chunks[1:]]

    return draws, cards


with open("2021/day-04/example.txt", encoding="utf-8") as f:
    input = [str(line.strip()) for line in f]
    draws, cards = parse_input(input)

    assert 4512 == play_to_win(draws, cards)
    assert 1924 == play_to_lose(draws, cards)


with open("2021/day-04/input.txt", encoding="utf-8") as f:
    input = [str(line.strip()) for line in f]
    draws, cards = parse_input(input)
    print("Part 1: Bingo winner score is", play_to_win(draws, cards))
    print("Part 2: Bingo loser score is", play_to_lose(draws, cards))
