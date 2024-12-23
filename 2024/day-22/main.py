import sys
from typing import List
sys.path.insert(0, './')
from utils import profiler, DIRECTIONS

def mix(secret: int, number: int) -> int:
    return secret ^ number

def prune(secret: int) -> int:
    return secret % 16777216

def next_secret(secret: int) -> int:
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret

@profiler
def calculate_buyer_score(secrets: List[int]) -> int:
    results = []
    for secret in secrets:
        for _ in range(2000):
            secret = next_secret(secret)
        results.append(secret)

    return sum(results)

with open("2024/day-22/example.txt", encoding="utf-8") as f:
    secrets = list(map(int, f.readlines()))

    assert 37327623 == calculate_buyer_score(secrets)

with open("2024/day-22/input.txt", encoding="utf-8") as f:
    secrets = list(map(int, f.readlines()))

    print(f"Part 1: Output of the program is {calculate_buyer_score(secrets)}")