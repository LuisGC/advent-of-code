def count_positive_answer (input: str) -> int:
    positive_answers = 0

    for group in input.split("\n\n"):
        people = group.split("\n")
        yeses = {c for person in people for c in person}
        positive_answers += len(yeses)

    return positive_answers

with open("day-06/example.txt") as f:
    input =f.read()
    assert 11 == count_positive_answer(input)
