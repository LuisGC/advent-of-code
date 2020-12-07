from typing import NamedTuple, Dict, List, Tuple
from collections import defaultdict

class Bag(NamedTuple):
    color: str
    contains: Dict[str, int]

def parse_bag(line: str) -> Bag:
    container_part, content_part = line.split(" contain ")
    color = container_part[:-5]

    content_part = content_part.rstrip(".")
    content = {}

    if content_part != "no other bags":
        content_list = content_part.split(",")

        for bag in content_list:
            bag_parts = bag.strip().split(" ")
            content[bag_parts[1] + " " + bag_parts[2]] = bag_parts [0]

    return Bag(color, content)

def parse_bags(raw: str) -> List[Bag]:
    return [parse_bag(line) for line in raw.split("\n")]

def convert_to_dict(bags):
    dict = defaultdict(list)
    for bag in bags:
        for child in bag.contains:
            dict[child].append(bag.color)
    return dict

def contain_color(bags: List[Bag], color: str) -> List[str]:
    is_contained_in_dict = convert_to_dict(bags)

    check_color = [color]
    contain_color_list = set()

    while check_color:
        color_to_check = check_color.pop()
        for item in is_contained_in_dict.get(color_to_check,[]):
            if item not in contain_color_list:
                contain_color_list.add(item)
                check_color.append(item)

    return list(contain_color_list)

def bags_inside(bags: List[Bag], color: str) -> int:
    by_color = {bag.color: bag for bag in bags}

    bags_inside = 0
    stack: List[Tuple[str, int]] = [(color, 1)]
    while stack:
        next_color, multiplier = stack.pop()
        bag = by_color[next_color]
        for child, count in bag.contains.items():
            bags_inside += multiplier * int(count)
            stack.append((child, int(count) * multiplier))

    return bags_inside

with open("day-07/example.txt") as f:
    bags = parse_bags(f.read().strip())
    assert 4 == len(contain_color(bags, "shiny gold"))
    assert 32 == bags_inside(bags, "shiny gold")

with open("day-07/input.txt") as f:
    bags = parse_bags(f.read().strip())
    print("Part 1:", len(contain_color(bags, "shiny gold")), "bags can contain a shiny gold bag")
    print("Part 2: a shiny gold bag contains", bags_inside(bags, "shiny gold"), "bags")
