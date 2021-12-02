from __future__ import annotations
from typing import NamedTuple, List, Dict, Set


class MenuItem(NamedTuple):
    ingredients: List[str]
    allergens: List[str]

    @staticmethod
    def parse(line: str) -> MenuItem:
        parts = line.strip().split("(contains ")

        if len(parts) == 1:
            allergens = []
        else:
            allergens = parts[1][:-1].split(", ")
        return MenuItem(parts[0].split(), allergens)


def extract_ingredients_per_allergen(menuItems: List[MenuItem]) -> Dict[str, Set[str]]:
    ingredients_per_allergen: Dict[str, Set[str]] = {}

    for item in menuItems:
        for allergen in item.allergens:
            if allergen not in ingredients_per_allergen:
                ingredients_per_allergen[allergen] = set(item.ingredients)
            else:
                ingredients_per_allergen[allergen] = ingredients_per_allergen[allergen] & set(item.ingredients)

    allergens = list(ingredients_per_allergen)

    keep_going = True

    while keep_going:
        keep_going = False
        known = {allergen: cands
                 for allergen, cands in ingredients_per_allergen.items()
                 if len(cands) == 1}
        taken_ingredients = {ingredient
                             for ingredients in known.values()
                             for ingredient in ingredients}

        for allergen in allergens:
            if allergen not in known and (ingredients_per_allergen[allergen] & taken_ingredients):
                ingredients_per_allergen[allergen] = ingredients_per_allergen[allergen] - taken_ingredients
                keep_going = True

    return ingredients_per_allergen


def no_allergens(menuItems: List[MenuItem]) -> int:
    ingredients_per_allergen = extract_ingredients_per_allergen(menuItems)
    ingredients_with_allergen = {ingredient
                                 for ingredients_per_allergen in ingredients_per_allergen.values()
                                 for ingredient in ingredients_per_allergen}

    return sum(ingredient not in ingredients_with_allergen
               for menuItem in menuItems
               for ingredient in menuItem.ingredients)


def arrange(ingredients_per_allergen: Dict[str, Set[str]]) -> str:
    return ",".join(next(iter(ingredients))
                    for allergen, ingredients in sorted(ingredients_per_allergen.items()))


with open("2020/day-21/example.txt") as f:
    menu_list = [MenuItem.parse(line) for line in f.readlines()]
    free_of_allergens = no_allergens(menu_list)
    assert 5 == free_of_allergens
    ingredients_per_allergen = extract_ingredients_per_allergen(menu_list)
    assert "mxmxvkd,sqjhc,fvjkl" == arrange(ingredients_per_allergen)

with open("2020/day-21/input.txt") as f:
    menu_list = [MenuItem.parse(line) for line in f.readlines()]
    free_of_allergens = no_allergens(menu_list)
    print("Part 1: The ingredients free of allergens appear (times): ",
          free_of_allergens)
    ingredients_per_allergen = extract_ingredients_per_allergen(menu_list)
    print("Part 2: The canonical dangerous ingredient list is: ",
          arrange(ingredients_per_allergen))
