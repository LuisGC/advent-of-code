from typing import List, NamedTuple, Tuple


Range = Tuple[int, int]


class Rule(NamedTuple):
    name: str
    ranges: Tuple[Range, Range]


def create_range(text: str) -> Range:
    return (int(text.split("-")[0]), int(text.split("-")[1]))


def parse_rule(raw_rule: str) -> List[int]:
    name, ranges = raw_rule.split(": ")
    r1, r2 = ranges.split(" or ")

    return Rule(
                name=name,
                ranges=[create_range(r1), create_range(r2)]
                )


def parse_ticket(raw_ticket: str) -> List[int]:
    return [int(n) for n in raw_ticket.split(",")]


def parse_input(notes: str):

    a, b, c = notes.strip().split("\n\n")
    b = b.split("\n")[-1]

    rules = [parse_rule(line) for line in a.split("\n")]
    my_ticket = parse_ticket(b)
    nearby_tickets = [parse_ticket(line) for line in c.split("\n")[1:]]

    return rules, my_ticket, nearby_tickets


def is_valid_value(value: int, rule: Rule) -> bool:
    return (rule.ranges[0][0] <= value <= abs(rule.ranges[0][1])
            or rule.ranges[1][0] <= value <= rule.ranges[1][1])


def error_rate(rules: List[Rule], tickets: List[int]) -> int:
    errors = 0

    for ticket in tickets:
        for value in ticket:
            valid = False

            for rule in rules:
                if is_valid_value(value, rule):
                    valid = True
                    break

            if not valid:
                errors += value

    return errors


def is_valid_ticket(rules: List[int], ticket: List[int]) -> bool:
    for n in ticket:
        if not any(is_valid_value(n, rule) for rule in rules):
            return True
    return False


def get_valid_tickets(rules: List[int], tickets: List[int]) -> List[int]:
    valid_tickets = [
        t for t in tickets if not is_valid_ticket(rules, t)
    ]

    return valid_tickets


def get_departure_fields(rules: List[int],
                         my_ticket: List[int],
                         valid_tickets: List[int]):

    return 1*1*1*1


with open("day-16/example.txt") as f:
    rules, my_ticket, nearby_tickets = parse_input(f.read())
    assert 71 == error_rate(rules, nearby_tickets)
    valid_tickets = get_valid_tickets(rules, nearby_tickets)

with open("day-16/input.txt") as f:
    rules, my_ticket, nearby_tickets = parse_input(f.read())
    print("Part 1: Error rate is: ", error_rate(rules, nearby_tickets))
    valid_tickets = get_valid_tickets(rules, nearby_tickets)
    print("Part 2: The departure values multiplied is: ",
          get_departure_fields(rules, my_ticket, nearby_tickets))
