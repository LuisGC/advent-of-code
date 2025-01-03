from collections import defaultdict
from typing import List

def parse_input(input_lines: List[str]) -> defaultdict:
    connections = []
    for line in input_lines:
        a, b = line.split("-")
        connections.append((a, b))

    lan_dict = defaultdict(set)
    for a, b in connections:
        lan_dict[a].add(b)
        lan_dict[b].add(a)

    return lan_dict

class LanGroup:
    def __init__(self, members: List[str]):
        self.members = members
        self.members.sort()

    def __eq__(self, other):
        return self.members == other.members
    
    def __hash__(self):
        return hash(",".join(self.members))

def lan_parties_filter(lan_dict: defaultdict, code: str = "t") -> int:
    lan_parties = set()
    for me, mine in lan_dict.items():
        for other in mine:
            for common in lan_dict[other]:
                if common in mine and common not in [me, other]:
                    lan_parties.add(LanGroup([me, other, common]))

    return len([party for party in lan_parties if any(member.startswith(code) for member in party.members)])

def membersInterconnected(lan_party: LanGroup) -> bool:
    members = lan_party.members
    for member in members:
        my_connections = lan_dict[member]
        for other in members:
            if other not in my_connections and other != member:
                return False
    return True

def largest_party(lan_dict: defaultdict) -> str:
    lan_parties = set()
    for me, mine in lan_dict.items():
        for other in mine:
            lan_parties.add(LanGroup([me, other] + [x for x in lan_dict[other] if x in mine]))

    interconnected_parties = [it.members for it in (filter(membersInterconnected, list(lan_parties)))]
    largest_party = sorted(interconnected_parties, key=lambda party: len(party)).pop()

    return ",".join(largest_party)


with open("2024/day-23/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    lan_dict = parse_input(input_lines)

    assert 7 == lan_parties_filter(lan_dict)

    assert "co,de,ka,ta" == largest_party(lan_dict)

with open("2024/day-23/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    lan_dict = parse_input(input_lines)

    print(f"Part 1: Lan parties with filter is {lan_parties_filter(lan_dict)}")
    print(f"Part 2: Largest interconnected LAN party is {largest_party(lan_dict)}")