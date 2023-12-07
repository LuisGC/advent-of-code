from typing import List, Tuple
from functools import cmp_to_key

CARDS = list('AKQJT98765432')[::-1]
CARDS_WITH_JOKER = list('AKQT98765432J')[::-1]

def parse_input (lines: List[str]) -> List[Tuple]:
    return [line.split() for line in lines if len(line) > 0]

def categorize_hand(hand: Tuple) -> int:
  if len(set(hand)) == 1:
    return 7
  elif len(set(hand)) == 2:
    a,b = set(hand)
    if hand.count(a) == 4 or hand.count(b) == 4:
      return 6
    elif hand.count(a) == 3 or hand.count(b) == 3:
      return 5
  elif len(set(hand)) == 3:
    a,b,c = set(hand)
    a,b,c = [hand.count(v) for v in [a,b,c]]
    if a == 3 or b == 3 or c == 3:
      return 4
    if set([a,b,c]) == {2,2,1}:
      return 3
  elif len(set(hand)) == 4:
    return 2
  return 1

def compare_hands(a: Tuple, b: Tuple) -> int:
    a,_ = a
    b,_ = b
    cha = categorize_hand(a)
    chb = categorize_hand(b)
    if cha > chb:
      return 1
    elif cha < chb:
      return -1
    for ca, cb in zip(a,b):
      if CARDS.index(ca) > CARDS.index(cb):
        return 1
      elif CARDS.index(ca) < CARDS.index(cb):
        return -1
    return 0

def categorize_hand_with_joker(hand: Tuple):
  max_value = None
  for c in CARDS_WITH_JOKER:
    replaced_hand = hand.replace('J',c)
    replaced_value = categorize_hand(replaced_hand)
    if max_value is None or replaced_value > max_value:
      max_value = replaced_value
  return max_value

def compare_hands_with_jokers(a: Tuple, b: Tuple) -> int:
    a,_ = a
    b,_ = b
    cha = categorize_hand_with_joker(a)
    chb = categorize_hand_with_joker(b)
    if cha > chb:
      return 1
    elif cha < chb:
      return -1
    for ca, cb in zip(a,b):
      if CARDS_WITH_JOKER.index(ca) > CARDS_WITH_JOKER.index(cb):
        return 1
      elif CARDS_WITH_JOKER.index(ca) < CARDS_WITH_JOKER.index(cb):
        return -1
    return 0

def total_winnings(hands: List[Tuple], jokers: bool= False) -> int:
    if jokers:
        hands.sort(key=cmp_to_key(compare_hands_with_jokers))
    else:
        hands.sort(key=cmp_to_key(compare_hands))

    winnings = 0
    for i, (h, bid) in enumerate(hands):
        winnings += int(bid)*(i+1)

    return winnings


with open("2023/day-07/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    hands = parse_input(input_lines)

    assert 6440 == total_winnings(hands)
    assert 5905 == total_winnings(hands, jokers=True)
    

with open("2023/day-07/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    hands = parse_input(input_lines)
    print("Part 1: Total winnings are ", total_winnings(hands))
    print("Part 2: Total winnings with Jokers are ", total_winnings(hands, jokers=True))
