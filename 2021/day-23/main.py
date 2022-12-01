from typing import List
from sys import maxsize

COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

class Burrow:
    def __init__(self, room_size: int = 2):
        self.cavern = ['.'] * 11
        self.room_size = room_size
        self.goal = [
            '.', '.', 'A' * self.room_size, '.', 'B' * self.room_size, '.',
            'C' * self.room_size, '.', 'D' * self.room_size, '.', '.'
        ]
        self.destination = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
        self.destination_set = set(self.destination.values())

    def add_line(self, line: str):
        for pos, char in enumerate(line):
            if char in ['A', 'B', 'C', 'D']:
                if self.cavern[pos - 1] != '.':
                    self.cavern[pos - 1] += char
                else:
                    self.cavern[pos - 1] = char

    def __repr__(self):
        return f'{self.cavern}'

    def get_piece_from_room(self, room: str):
        for char in room:
            if char != '.':
                return char

    def add_to_room(self, char: str, room: str):
        room = list(room)
        distance = room.count('.')
        room[distance - 1] = char
        return ''.join(room), distance

    def can_reach(self, cavern: List, position: int, destination: int):
        for i in range(min(position, destination), max(position, destination) + 1):
            if i == position:
                continue
            if i in self.destination_set:
                continue
            if cavern[i] != '.':
                return False
        return True

    def room_ok(self, cavern: List, piece: str, destination: int):
        in_room = cavern[destination]
        return len(in_room) == in_room.count('.') + in_room.count(piece)

    def possible_moves(self, cavern: List, position: int):
        piece = cavern[position]
        if position not in self.destination_set:
            dest = self.destination[piece]
            if self.can_reach(cavern, position, dest) and self.room_ok(cavern, piece, dest):
                return [dest]
            
            return []
        moving_letter = self.get_piece_from_room(piece)
        if position == self.destination[moving_letter] and self.room_ok(cavern, moving_letter, position):
            return []

        possible = []
        for dest in range(len(cavern)):
            if dest == position:
                continue
            if dest in self.destination_set and self.destination[moving_letter] != dest:
                continue
            if self.destination[moving_letter] == dest:
                if not self.room_ok(cavern, moving_letter, dest):
                    continue
            if self.can_reach(cavern, position, dest):
                possible.append(dest)

        return possible


    def move(self, cavern: List, position: int, destination: int):
        new_cavern = cavern[:]
        distance = 0
        moving_char = self.get_piece_from_room(cavern[position])
        if len(cavern[position]) == 1:
            new_cavern[position] = '.'
        else:
            new_room = ''
            found = False
            for c in cavern[position]:
                if c == '.':
                    distance += 1
                    new_room += c
                elif not found:
                    new_room += '.'
                    distance += 1
                    found = True
                else:
                    new_room += c
            new_cavern[position] = new_room
        distance += abs(position - destination)

        if len(cavern[destination]) == 1:
            new_cavern[destination] = moving_char
        else:
            new_cavern[destination], additional_distance = self.add_to_room(moving_char, cavern[destination])
            distance += additional_distance

        return new_cavern, distance * COSTS[moving_char]

    def solve(self):
        states = {tuple(self.cavern): 0}
        queue = [self.cavern]

        while queue:
            cavern = queue.pop()
            for pos, piece in enumerate(cavern):
                if self.get_piece_from_room(piece) is None:
                    continue
                destinations = self.possible_moves(cavern, pos)
                for dest in destinations:
                    new_cavern, additional_cost = self.move(cavern, pos, dest)
                    new_cost = states[tuple(cavern)] + additional_cost
                    new_cavern_tuple = tuple(new_cavern)
                    cost = states.get(new_cavern_tuple, maxsize)
                    if new_cost < cost:
                        states[new_cavern_tuple] = new_cost
                        queue.append(new_cavern)
        
        return states[tuple(self.goal)]


def process_input(input_lines: List, room_size: int = 2) -> Burrow:
    burrow = Burrow(room_size)
    for line in input_lines:
        burrow.add_line(line)

    # print(burrow)
    return burrow


with open("2021/day-23/example.txt") as f:
    burrow = process_input([line for line in f])
    assert 12521 == burrow.solve()

with open("2021/day-23/input.txt") as f:
    burrow = process_input([line for line in f])
    print("Part 1: The minimum energy is:", burrow.solve())

with open("2021/day-23/unfolded_example.txt") as f:
    burrow = process_input([line for line in f], 4)
    assert 44169 == burrow.solve()

# with open("2021/day-23/unfolded_input.txt") as f:
#     burrow = process_input([line for line in f], 4)
#     print("Part 2: The minimum energy is:", burrow.solve())
