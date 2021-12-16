from math import prod

class Packet:
    def __init__(self, message: str):
        self.version = int(message[:3], 2)
        self.type = int(message[3:6], 2)
        self.length = 0
        self.subpackets = []

        if self.type == 4: # literal
            self.length = 3 + 3
            value = ""
            while True:
                value += message[self.length + 1 : self.length + 5]
                self.length += 5
                if message[self.length - 5] == "0":
                    break
            self.value = int(value, 2)
        else: #operator
            length_type = message[6]
            if length_type == "0":
                LENGTH = 3 + 3 + 1 + 15
                total_length = int(message[7:LENGTH], 2)
                self.length = LENGTH
                while self.length != LENGTH + total_length:
                    subpacket = Packet(message[self.length :])
                    self.subpackets.append(subpacket)
                    self.length += subpacket.length
            elif length_type == "1":
                LENGTH = 3 + 3 + 1 + 11
                amount_subpackets = int(message[7:LENGTH], 2)
                self.length = LENGTH
                for sp in range(amount_subpackets):
                    subpacket = Packet(message[self.length :])
                    self.subpackets.append(subpacket)
                    self.length += subpacket.length
            else:
                raise Exception("unknown length_type", length_type)

    def evaluate(self) -> int:
        if self.type == 4: # literal
            return self.value
        elif self.type == 0:
            return sum(p.evaluate() for p in self.subpackets)
        elif self.type == 1:
            return prod(p.evaluate() for p in self.subpackets)
        elif self.type == 2:
            return min(p.evaluate() for p in self.subpackets)
        elif self.type == 3:
            return max(p.evaluate() for p in self.subpackets)
        elif self.type == 5:
            return self.subpackets[0].evaluate() > self.subpackets[1].evaluate()
        elif self.type == 6:
            return self.subpackets[0].evaluate() < self.subpackets[1].evaluate()
        elif self.type == 7:
            return self.subpackets[0].evaluate() == self.subpackets[1].evaluate()
        else:
            raise Exception("unknown type ID", self.type)


def count_versions(packet : Packet) -> int:
    return packet.version + sum(count_versions(subpacket) for subpacket in packet.subpackets)


def solve_part_1(message: str) -> int:
    message_bin = bin(int("1" + message, 16))[3:]
    return count_versions(Packet(message_bin))


def solve_part_2(message: str) -> int:
    message_bin = bin(int("1" + message, 16))[3:]
    return Packet(message_bin).evaluate()


with open("2021/day-16/example.txt") as f:
    lines = [line.strip() for line in f]
    assert 16 == solve_part_1(lines[0])
    assert 12 == solve_part_1(lines[1])
    assert 23 == solve_part_1(lines[2])
    assert 31 == solve_part_1(lines[3])

with open("2021/day-16/example-eval.txt") as f:
    lines = [line.strip() for line in f]
    assert 3 == solve_part_2(lines[0])
    assert 54 == solve_part_2(lines[1])
    assert 7 == solve_part_2(lines[2])
    assert 9 == solve_part_2(lines[3])
    assert 1 == solve_part_2(lines[4])
    assert 0 == solve_part_2(lines[5])
    assert 0 == solve_part_2(lines[6])
    assert 1 == solve_part_2(lines[7])

with open("2021/day-16/input.txt") as f:
    lines = [line.strip() for line in f]
    message = bin(int("1" + lines[0], 16))[3:]
    packet = Packet(message)
    print("Part 1: Sum of all versions is:", count_versions(packet))
    print("Part 2: Result after evaluating is:", packet.evaluate())
