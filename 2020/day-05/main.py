from typing import NamedTuple


class Seat(NamedTuple):
    row: int
    col: int

    @property
    def id(self) -> int:
        return self.row * 8 + self.col


def parse_seat(boarding_pass: str) -> Seat:
    row = 0
    col = 0

    for i, c in enumerate(boarding_pass[:7]):
        multiplier = 2 ** (6 - i)
        include = 1 if c == 'B' else 0
        row += multiplier * include

    for i, c in enumerate(boarding_pass[-3:]):
        multiplier = 2 ** (2 - i)
        include = 1 if c == 'R' else 0
        col += multiplier * include

    return Seat(row, col)


with open("day-05/example.txt") as f:
    seats = [parse_seat(seat.strip()) for seat in f]
    assert 820 == max(seat.id for seat in seats)


with open("day-05/input.txt") as f:
    seats = [parse_seat(seat.strip()) for seat in f]
    print("Part 1\nMax seat number:", max(seat.id for seat in seats))

    seat_ids = [seat.id for seat in seats]

    lo = min(seat_ids)
    hi = max(seat_ids)

    print("Part 2\nMissing seat number:", [x for x in range(lo, hi)
                                           if x not in seat_ids][0])
