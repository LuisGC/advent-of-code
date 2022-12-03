from typing import List, Set
import itertools


def parse_input(input: str) -> (List[str], List[str]):
    block1, block2 = input.strip().split("\n\n")

    p1_cards = [int(line.strip()) for line in block1.split("\n")[1:]]
    p2_cards = [int(line.strip()) for line in block2.split("\n")[1:]]

    return p1_cards, p2_cards


def play_space_cards(p1_cards: List[int],
                     p2_cards: List[int]) -> (List[int], List[int]):

    while p1_cards and p2_cards:
        a = p1_cards[0]
        b = p2_cards[0]

        if a > b:
            p1_cards = p1_cards[1:] + [a, b]
            p2_cards = p2_cards[1:]
        else:
            p2_cards = p2_cards[1:] + [b, a]
            p1_cards = p1_cards[1:]

    return p1_cards, p2_cards


def scoring(p1_cards: List[int],
            p2_cards: List[int]) -> int:

    winner = p1_cards if p1_cards else p2_cards

    return sum(card * i for card, i in zip(reversed(winner), itertools.count(1)))


def play_recursive_game(p1_cards: List[int],
                        p2_cards: List[int],
                        played: Set[int]) -> (List[int], List[int]):

    while p1_cards and p2_cards:
        t = (tuple(p1_cards), tuple(p2_cards))

        if t in played:
            return (p1_cards, p2_cards)

        played.add(t)

        a = p1_cards[0]
        b = p2_cards[0]
        p1_cards = p1_cards[1:]
        p2_cards = p2_cards[1:]

        if a > len(p1_cards) or b > len(p2_cards):
            if a > b:
                p1_cards += [a, b]
            else:
                p2_cards += [b, a]
            continue

        recplay1, _ = play_recursive_game(p1_cards[:a], p2_cards[:b], set())

        if recplay1:
            p1_cards += [a, b]
        else:
            p2_cards += [b, a]

    return (p1_cards, p2_cards)


with open("2020/day-22/example.txt", encoding="utf-8") as f:
    p1_cards, p2_cards = parse_input(f.read())
    p1_end_cards, p2_end_cards = play_space_cards(p1_cards, p2_cards)
    assert len(p1_cards) + len(p2_cards) == len(p1_end_cards) + len(p2_end_cards)
    assert 306 == scoring(p1_end_cards, p2_end_cards)

    p1_end_cards, p2_end_cards = play_recursive_game(p1_cards, p2_cards, set())
    assert len(p1_cards) + len(p2_cards) == len(p1_end_cards) + len(p2_end_cards)

    assert 291 == scoring(p1_end_cards, p2_end_cards)


with open("2020/day-22/input.txt", encoding="utf-8") as f:
    p1_cards, p2_cards = parse_input(f.read())
    p1_end_cards, p2_end_cards = play_space_cards(p1_cards, p2_cards)
    assert len(p1_cards) + len(p2_cards) == len(p1_end_cards) + len(p2_end_cards)
    print("Part 1: Scoring of the winner in Space Cards is: ",
          scoring(p1_end_cards, p2_end_cards))
    p1_end_cards, p2_end_cards = play_recursive_game(p1_cards, p2_cards, set())
    assert len(p1_cards) + len(p2_cards) == len(p1_end_cards) + len(p2_end_cards)
    print("Part 2: Scoring of the winner in Recursive mode is: ",
          scoring(p1_end_cards, p2_end_cards))
