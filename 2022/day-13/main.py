from typing import List
from math import prod
from functools import cmp_to_key

def compare_packets(left, right) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    elif isinstance(left, list) and isinstance(right, list):
        for inner_left, inner_right in zip(left, right):
            if (ret := compare_packets(inner_left, inner_right)) != 0:
                return ret
        return compare_packets(len(left), len(right))
    else:
        if isinstance(left, list):
            return compare_packets(left, [right])
        elif isinstance(right, list):
            return compare_packets([left], right)

def pairs_in_order(packets: List) -> List:
    right_pairs = []
    for i, (left, right) in enumerate(zip(packets[::2], packets[1::2])):
        if compare_packets(left, right) <= 0:
            right_pairs.append(i + 1)
    return right_pairs

def sort_packets(packets: List) -> List:
    keys = [[[2]], [[6]]]
    keys_index = []
    for i, packet in enumerate(sorted(packets + keys, key=cmp_to_key(compare_packets))):
        if packet in keys:
            keys_index.append(i + 1)

    return keys_index

with open("2022/day-13/example.txt", encoding="utf-8") as f:
    packets = [eval(line) for line in f.read().splitlines() if len(line)]

    assert 13 == sum(pairs_in_order(packets))
    assert 140 == prod(sort_packets(packets))

with open("2022/day-13/input.txt", encoding="utf-8") as f:
    packets = [eval(line) for line in f.read().splitlines() if len(line)]

    print("Part 1: Sum of indices of pairs in rigth order:", sum(pairs_in_order(packets)))
    print("Part 2: Prod of indices of key packets:", prod(sort_packets(packets)))
