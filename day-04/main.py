from typing import Dict, List
import re

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

def is_valid_height(hgt: str) -> bool:
    if hgt.endswith('cm'):
        hgt = hgt.replace('cm', '')
        try:
            return 150 <= int(hgt) <= 193
        except:
            return False
    elif hgt.endswith("in"):
        hgt = hgt.replace("in", "")
        try:
            return 59 <= int(hgt) <= 76
        except:
            return False

    return False

def is_valid_and_correct(passport: Passport) -> bool:
    quality_checks = [
        1920 <= int(passport.get('byr', -1)) <= 2002,
        2010 <= int(passport.get('iyr', -1)) <= 2020,
        2020 <= int(passport.get('eyr', -1)) <= 2030,
        is_valid_height(passport.get('hgt', '')),
        re.match(r"^#[0-9a-f]{6}$", passport.get('hcl', '')),
        passport.get('ecl') in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
        re.match(r"^[0-9]{9}$", passport.get('pid', ''))
    ]

    return is_valid(passport) and all(quality_checks);

with open("day-04/example.txt") as f:
    passports = parse_list(f.read())
    assert 2 == sum(is_valid(passport) for passport in passports)

with open("day-04/invalid.txt") as f:
    passports = parse_list(f.read())
    assert all(is_valid(passport) for passport in passports)
    assert not any(is_valid_and_correct(passport) for passport in passports)

with open("day-04/valid.txt") as f:
    passports = parse_list(f.read())
    assert all(is_valid(passport) for passport in passports)
    assert all(is_valid_and_correct(passport) for passport in passports)

with open("day-04/input.txt") as f:
    passports = parse_list(f.read())
    print("Amount of Passports", len(passports))
    print("Part 1 - Valid Passports", sum(is_valid(passport) for passport in passports))
    print("Part 2 - Valid and correct Passports", sum(is_valid_and_correct(passport) for passport in passports))
