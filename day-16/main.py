from typing import List, NamedTuple, Tuple


Range = Tuple[int, int]


class Rule(NamedTuple):
    name: str
    ranges: Tuple[Range, Range]
    position: int


Ticket = List[int]


def create_range(text: str) -> Range:
    return (int(text.split("-")[0]), int(text.split("-")[1]))


def parse_rule(raw_rule: str, num_positions: int) -> Rule:
    name, ranges = raw_rule.split(": ")
    r1, r2 = ranges.split(" or ")

    return Rule(name=name,
                ranges=[create_range(r1), create_range(r2)],
                position=list(range(0, num_positions)))


def parse_ticket(raw_ticket: str) -> Ticket:
    return [int(n) for n in raw_ticket.split(",")]


def parse_input(notes: str):

    a, b, c = notes.strip().split("\n\n")
    b = b.split("\n")[-1]
    my_ticket = parse_ticket(b)

    rules = [parse_rule(line, len(my_ticket)) for line in a.split("\n")]
    nearby_tickets = [parse_ticket(line) for line in c.split("\n")[1:]]

    return rules, my_ticket, nearby_tickets


def is_valid_value(value: int, rule: Rule) -> bool:
    return any(lo <= value <= hi for lo, hi in rule.ranges)


def error_rate(rules: List[Rule], tickets: List[Ticket]) -> int:
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


def is_valid_ticket(rules: List[Rule], ticket: Ticket) -> bool:
    for n in ticket:
        if not any(is_valid_value(n, rule) for rule in rules):
            return True
    return False


def get_valid_tickets(rules: List[Rule], tickets: List[Ticket]) -> List[int]:
    valid_tickets = [
        t for t in tickets if not is_valid_ticket(rules, t)
    ]

    return valid_tickets


def remove_position_from_other_keys(rules, rule_to_keep, position_to_remove):
    for rule in rules:
        if (rule.name != rule_to_keep.name and
                position_to_remove in rule.position and
                position_to_remove in rule_to_keep.position):
            rule.position.remove(position_to_remove)


def get_departure_fields(rules: List[int],
                         my_ticket: Ticket,
                         nearby_tickets: List[Ticket]):
    valid_tickets = get_valid_tickets(rules, nearby_tickets)

    for ticket in valid_tickets:
        for i in range(0, len(ticket)):
            for rule in rules:
                if not is_valid_value(ticket[i], rule):
                    if i in rule.position:
                        rule.position.remove(i)

                if len(rule.position) == 1:
                    remove_position_from_other_keys(rules,
                                                    rule,
                                                    rule.position[0])

        if all(len(rule.position) == 1 for rule in rules):
            break

    departure_values = [
        rule.position[0]
        for rule in rules
        if rule.name.startswith('departure')
        ]

    assert 6 == len(departure_values)

    val = 1
    for dep_position in departure_values:
        val *= my_ticket[dep_position]

    return val


with open("day-16/example.txt") as f:
    rules, my_ticket, nearby_tickets = parse_input(f.read())
    assert 71 == error_rate(rules, nearby_tickets)

with open("day-16/input.txt") as f:
    rules, my_ticket, nearby_tickets = parse_input(f.read())
    print("Part 1: Error rate is: ", error_rate(rules, nearby_tickets))
    print("Part 2: The departure values multiplied is: ",
          get_departure_fields(rules, my_ticket, nearby_tickets))
