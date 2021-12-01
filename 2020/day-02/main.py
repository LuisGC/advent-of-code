class Password_item:
    min: int
    max: int
    char: str
    password: str

    def __init__(self, min, max, char, password):
        self.min = min
        self.max = max
        self.char = char
        self.password = password

    def is_valid(self) -> bool:
        return self.min <= self.password.count(self.char) <= self.max

    def is_valid_2(self) -> bool:
        char_in_min = self.password[self.min-1] == self.char
        char_in_max = self.password[self.max-1] == self.char
        return char_in_min != char_in_max

    def line2Password(line):
        limits, char, password = line.strip().split()
        lo, hi = [int(n) for n in limits.split("-")]
        char = char[0]

        return Password_item(lo, hi, char, password)


with open("day-02/example.txt") as f:
    passwords = [Password_item.line2Password(line) for line in f]
    assert 2 == sum(pw.is_valid() for pw in passwords)


with open("day-02/input.txt") as f:
    passwords = [Password_item.line2Password(line) for line in f]
    print("Part 1:", sum(pw.is_valid() for pw in passwords))

with open("day-02/example.txt") as f:
    passwords = [Password_item.line2Password(line) for line in f]
    assert 1 == sum(pw.is_valid_2() for pw in passwords)

with open("day-02/input.txt") as f:
    passwords = [Password_item.line2Password(line) for line in f]
    print("Part 2:", sum(pw.is_valid_2() for pw in passwords))
