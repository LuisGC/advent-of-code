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
            self.value = self.evaluate()

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


def text_to_packet(message: str) -> int:
    message_bin = bin(int("1" + message, 16))[3:]
    return Packet(message_bin)


def count_versions(packet : Packet) -> int:
    return packet.version + sum(count_versions(subpacket) for subpacket in packet.subpackets)


assert 16 == count_versions(text_to_packet("8A004A801A8002F478"))
assert 12 == count_versions(text_to_packet("620080001611562C8802118E34"))
assert 23 == count_versions(text_to_packet("C0015000016115A2E0802F182340"))
assert 31 == count_versions(text_to_packet("A0016C880162017C3686B18A3D4780"))

assert 3 == text_to_packet("C200B40A82").value
assert 54 == text_to_packet("04005AC33890").value
assert 7 == text_to_packet("880086C3E88112").value
assert 9 == text_to_packet("CE00C43D881120").value
assert 1 == text_to_packet("D8005AC2A8F0").value
assert 0 == text_to_packet("F600BC2D8F").value
assert 0 == text_to_packet("9C005AC2F8F0").value
assert 1 == text_to_packet("9C0141080250320F1802104A08").value


with open("2021/day-16/input.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f]
    packet = text_to_packet(lines[0])
    print("Part 1: Sum of all versions is:", count_versions(packet))
    print("Part 2: Result after evaluating is:", packet.value)
