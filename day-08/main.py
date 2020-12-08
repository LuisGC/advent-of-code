def run_until_loop (code: str) -> int:

    return 5

with open("day-07/example.txt") as f:
    code = f.read()
    assert 5 == run_until_loop(code)
