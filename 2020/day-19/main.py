from __future__ import annotations
from typing import NamedTuple, List, Optional
from collections import deque


class Rule(NamedTuple):
    id: int
    fixed_char: Optional[str] = None
    subrules: List[List[int]] = []

    @staticmethod
    def parse(line: str) -> Rule:
        rule_id, rest = line.strip().split(": ")
        if rest.startswith('"'):
            return Rule(id=int(rule_id),
                        fixed_char=rest[1:-1])

        if "|" in rest:
            parts = rest.split(" | ")
        else:
            parts = [rest]

        return Rule(id=int(rule_id),
                    subrules=[[int(n) for n in part.split()] for part in parts])


def parse_input(input: str):
    part_1, part_2 = input.split("\n\n")
    rules_dict = {}
    for rule_str in part_1.split("\n"):
        rule = Rule.parse(rule_str)
        rules_dict[rule.id] = rule
    return rules_dict, part_2.strip().split("\n")


def check(rules: dict[Rule], message: str) -> bool:

    pending_checks = deque([(message, [0])])

    while pending_checks:
        message, rule_ids = pending_checks.popleft()

        if not message and not rule_ids:
            return True

        if not message or not rule_ids:
            continue

        rule = rules[rule_ids[0]]
        rule_ids = rule_ids[1:]

        if rule.fixed_char and rule.fixed_char == message[0]:
            pending_checks.append((message[1:], rule_ids))

        else:
            for subrules_ids in rule.subrules:
                pending_checks.append((message, subrules_ids + rule_ids))

    return False


def matching_messages(rules: dict[Rule], messages: List[str]) -> List[bool]:
    return [check(rules, mess) for mess in messages]


with open("day-19/example.txt") as f:
    rules, messages = parse_input(f.read())
    matches = matching_messages(rules, messages)
    assert 2 == sum(matches)


with open("day-19/long-example.txt") as f:
    rules, messages = parse_input(f.read())
    matches = matching_messages(rules, messages)
    assert 3 == sum(matches)
    rules[8] = Rule(id=8,
                    subrules=[[42], [42, 8]])
    rules[11] = Rule(id=11,
                     subrules=[[42, 31], [42, 11, 31]])
    matches = matching_messages(rules, messages)
    assert 12 == sum(matches)


with open("day-19/input.txt") as f:
    rules, messages = parse_input(f.read())
    matches = matching_messages(rules, messages)
    print("Part 1: Sum of messages that match the 0 rule is: ",
          sum(matches))
    rules[8] = Rule(id=8,
                    subrules=[[42], [42, 8]])
    rules[11] = Rule(id=11,
                     subrules=[[42, 31], [42, 11, 31]])
    matches = matching_messages(rules, messages)
    print("Part 2: Sum of messages that match the 0 rule after changing 8 and 11 is: ",
          sum(matches))
