from collections import Counter


def count_positive_answer(group: str) -> int:
    yeses = {c for person in group for c in person}
    yeses.discard("\n")
    return len(yeses)


def count_unanimous_answer(group: str) -> int:
    people = group.split("\n")
    yeses = Counter(c for person in people for c in person)
    return sum(count == len(people) for c, count in yeses.items())


with open("2020/day-06/example.txt", encoding="utf-8") as f:
    input = f.read().strip()
    assert 11 == sum(count_positive_answer(group)
                     for group in input.split("\n\n"))
    assert 6 == sum(count_unanimous_answer(group)
                    for group in input.split("\n\n"))


with open("2020/day-06/input.txt", encoding="utf-8") as f:
    input = f.read().strip()
    print("Part 1:",
          sum(count_positive_answer(group) for group in input.split("\n\n")))
    print("Part 2:",
          sum(count_unanimous_answer(group) for group in input.split("\n\n")))
