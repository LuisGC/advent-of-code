from typing import List, Tuple


def parse_rule(raw_rule: str) -> List[int]:
    name, ranges = raw_rule.split(": ")
    r1, r2 = ranges.split(" or ")

    return [int(r1.split("-")[0]), int(r1.split("-")[1]),
            int(r2.split("-")[0]), int(r2.split("-")[1])]


def parse_ticket(raw_ticket: str) -> List[int]:
    return [int(n) for n in raw_ticket.split(",")]


def parse_input(notes: str):

    a, b, c = notes.strip().split("\n\n")
    b = b.split("\n")[-1]

    rules = [parse_rule(line) for line in a.split("\n")]
    print(rules)
    my_ticket = parse_ticket(b)
    print(my_ticket)
    nearby_tickets = [parse_ticket(line) for line in c.split("\n")[1:]]
    print(nearby_tickets)

    return rules, my_ticket, nearby_tickets


def error_rate(rules: List[int], tickets: List[int]) -> int:
    errors = 0

    for ticket in tickets:
        for val in ticket:
            valid = False

            for rule in rules:
                print("Rule", rule, "Ticket", val)
                if (rule[0] <= val <= abs(rule[1])
                        or rule[2] <= val <= rule[3]):
                    valid = True
                    break

            if not valid:
                print("not valid --> +", val)
                errors += val

    print("Total errors:", errors)
    return errors


with open("day-16/example.txt") as f:
    rules, my_ticket, nearby_tickets = parse_input(f.read())
    assert 71 == error_rate(rules, nearby_tickets)


with open("day-16/input.txt") as f:
    rules, my_ticket, nearby_tickets = parse_input(f.read())
    print("Part 1: Error rate is: ", error_rate(rules, nearby_tickets))
