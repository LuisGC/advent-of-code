def count_positive_answer (group: str) -> int:
    yeses = {c for person in group for c in person}
    yeses.discard("\n")
    return len(yeses)

with open("day-06/example.txt") as f:
    input =f.read()
    assert 11 == sum(count_positive_answer(group) for group in input.split("\n\n"))
