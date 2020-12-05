from typing import Dict, List

Passport = Dict[str, str]

def parse_passport(input: str) -> Passport:
    lines = input.strip().split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    passport = {}

    for line in lines:
        for chunk in line.split(" "):
            key, value = chunk.split(":")
            passport[key] = value

    return passport

def parse_list(document_list: str) -> List[Passport]:
    chunks = document_list.split("\n\n")
    return [parse_passport(chunk) for chunk in chunks if chunk.strip()]

required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

def is_valid(passport: Passport) -> bool:
    return all(field in passport for field in required_fields);

with open("day-04/example.txt") as f:
    passports = parse_list(f.read())
    assert 2 == sum(is_valid(passport) for passport in passports)

with open("day-04/input.txt") as f:
    passports = parse_list(f.read())
    print("Part 1 \nAmount of Passports", len(passports))
    print("Valid Passports", sum(is_valid(passport) for passport in passports))
