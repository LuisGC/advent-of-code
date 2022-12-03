from typing import List


class DumboOctopus:
    def __init__(self, energy):
        self.has_flashed = False
        self.energy: int = energy


class Octopuses:
    def __init__(self, octopuses: [[DumboOctopus]]):
        self.board = octopuses
        self.total_flashes = 0
        self.steps = 0
        self.first_synchronous_flash = 0

    def step(self):
        for line in self.board:
            for cell in line:
                cell.energy += 1

        new_flashes = True

        while new_flashes:
            new_flashes = False
            for y in range(0, len(self.board)):
                for x in range(0, len(self.board[y])):

                    if self.board[y][x].energy > 9 and not self.board[y][x].has_flashed:
                        self.board[y][x].has_flashed = True
                        new_flashes = True

                        self.total_flashes += 1

                        if 0 < y and 0 < x:
                            self.board[y - 1][x - 1].energy += 1
                        if 0 < y:
                            self.board[y - 1][x].energy += 1
                        if 0 < y and x < len(self.board[0]) - 1:
                            self.board[y - 1][x + 1].energy += 1
                        if 0 < x:
                            self.board[y][x - 1].energy += 1
                        if x < 9:
                            self.board[y][x + 1].energy += 1
                        if y < 9 and 0 < x:
                            self.board[y + 1][x - 1].energy += 1
                        if y < 9:
                            self.board[y + 1][x].energy += 1
                        if y < 9 and x < 9:
                            self.board[y + 1][x + 1].energy += 1

        self.steps += 1

        synch_flash = True
        for line in self.board:
            for cell in line:
                if cell.has_flashed:
                    cell.has_flashed = False
                    cell.energy = 0
                else:
                    synch_flash = False

        if synch_flash:
            self.first_synchronous_flash = self.steps

    def __str__(self):
        string = ''
        for line in self.board:
            new_line = ''
            for num in line:
                new_line += str(num.energy)

            string += new_line + '\n'
        return string


def count_flashes_per_steps(octopuses: Octopuses, steps: int) -> int:
    for _ in range(0, steps):
        octopuses.step()

    return octopuses.total_flashes


def first_synchronous_flash(octopuses: Octopuses) -> int:

    looking_for_sync = True
    while looking_for_sync:
        octopuses.step()
        if octopuses.first_synchronous_flash:
            looking_for_sync = False

    return octopuses.first_synchronous_flash


def parse_input(input: List[str]) -> Octopuses:
    octopuses_array = []
    for line in input:
        row = []
        for num in line:
            row.append(DumboOctopus(int(num)))
        octopuses_array.append(row)

    return Octopuses(octopuses_array)


with open("2021/day-11/example.txt", encoding="utf-8") as f:
    octopuses  = parse_input([line.strip() for line in f])
    assert 1656 == count_flashes_per_steps(octopuses, 100)
    assert 195 == first_synchronous_flash(octopuses)

with open("2021/day-11/input.txt", encoding="utf-8") as f:
    octopuses  = parse_input([line.strip() for line in f])
    print("Part 1: Total flashes in 100 steps are : ", count_flashes_per_steps(octopuses, 100))
    print("Part 2: First synchronous flash is after (days): ", first_synchronous_flash(octopuses))
