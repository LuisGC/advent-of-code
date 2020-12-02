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

    def line2Password(line):
        limits, char, password = line.strip().split()
        lo, hi = [int(n) for n in limits.split("-")]
        char = char[0]

        return Password_item(lo, hi, char, password)


def valid_passwords(inputs):

    count = 0
    for item in inputs:
        pwd = Password_item.line2Password(item)
        if (pwd.is_valid()):
            count += 1

    return count

with open("day-02/example.txt") as f:
    inputs = [line.strip() for line in f]
    assert 2 == valid_passwords(inputs)

with open("day-02/input.txt") as f:
    inputs = [line.strip() for line in f]
    print ("Part 1:")
    print(valid_passwords(inputs))
