from typing import List

class DeterministicDie():
    def __init__(self, sides: int):
        self.numSides = sides
        self.next = 1
        self.numRolls = 0

    def roll(self):
        result = self.next
        self.next = (self.next + 1 ) % self.numSides
        self.numRolls += 1
        return result

class DiracDiceGame():
    def __init__(self, player1_start: int, player2_start: int, dieSides: int):
        self.player1_pos = player1_start
        self.player2_pos = player2_start
        self.score = [0, 0]
        self.die = DeterministicDie(dieSides)


    def move(self, pos):
        rolled_dies = self.die.roll() + self.die.roll() + self.die.roll()
        new_pos = pos + rolled_dies
        while new_pos > 10:
            new_pos -= 10
        return new_pos


    def play(self, win_score: int) -> (int, int):
        done = False
        while not done:
            self.player1_pos = self.move(self.player1_pos)
            self.score[0] += self.player1_pos
            if max(self.score) >= win_score:
                done = True
            else:
                self.player2_pos = self.move(self.player2_pos)
                self.score[1] += self.player2_pos
                if max(self.score) >= win_score:
                    done = True
        # print(f"Final Score: {self.score} Num Rolls {self.die.numRolls}")
        return min(self.score), self.die.numRolls


def quantum_play(player1_pos: int, player2_pos: int, player1_score: int, player2_score: int, cache: dict={}) -> List[int]:
    # print(f"Current Pos: {player1_pos} {player2_pos} {player1_score} {player2_score}")

    if player1_score >= 21:
        return [1, 0]
    if player2_score >= 21:
        return [0, 1]

    accum_score = [0, 0]

    for die1 in range(1, 4):
        for die2 in range(1, 4):
            for die3 in range(1, 4):
                # print(f"Current Score: {die1} {die2} {die3} {accum_score}")
                new_pos = ((player1_pos + die1 + die2 + die3 - 1) % 10) + 1
                new_score = player1_score + new_pos
                further_results = cache.get((player2_pos, new_pos, player2_score, player1_score), None)
                if not further_results:
                    further_results = quantum_play(player2_pos, new_pos, player2_score, player1_score, cache)
                    cache[(player2_pos, new_pos, player2_score, player1_score)] = further_results
                accum_score[0] += further_results[1]
                accum_score[1] += further_results[0]

    return accum_score


class DiracDiceQuantumGame():
    def __init__(self, player1_start: int, player2_start: int):
        self.player1_pos = player1_start
        self.player2_pos = player2_start
        self.score = [0, 0]
        self.wins = [0, 0]

    def move(self, is_p1: bool, die: int, player1_pos: int, player1_score: int, player2_pos: int, player2_score: int, win_modifier: int):
        if is_p1:
            player1_pos = (player1_pos + die) % 10
            player1_score += player1_pos + 1

            if player1_score >= 21:
                self.wins[0] += win_modifier
                return
        else:
            player2_pos = (player2_pos + die) % 10
            player2_score += player2_pos + 1

            if player2_score >= 21:
                self.wins[1] += win_modifier
                return

        self.move(not is_p1, 3, player1_pos, player1_score, player2_pos, player2_score, win_modifier)
        self.move(not is_p1, 4, player1_pos, player1_score, player2_pos, player2_score, win_modifier * 3)
        self.move(not is_p1, 5, player1_pos, player1_score, player2_pos, player2_score, win_modifier * 6)
        self.move(not is_p1, 6, player1_pos, player1_score, player2_pos, player2_score, win_modifier * 7)
        self.move(not is_p1, 7, player1_pos, player1_score, player2_pos, player2_score, win_modifier * 6)
        self.move(not is_p1, 8, player1_pos, player1_score, player2_pos, player2_score, win_modifier * 3)
        self.move(not is_p1, 9, player1_pos, player1_score, player2_pos, player2_score, win_modifier)

    def play(self):
        self.move(True, 3, self.player1_pos - 1, 0, self.player2_pos - 1, 0, 1)
        self.move(True, 4, self.player1_pos - 1, 0, self.player2_pos - 1, 0, 3)
        self.move(True, 5, self.player1_pos - 1, 0, self.player2_pos - 1, 0, 6)
        self.move(True, 6, self.player1_pos - 1, 0, self.player2_pos - 1, 0, 7)
        self.move(True, 7, self.player1_pos - 1, 0, self.player2_pos - 1, 0, 6)
        self.move(True, 8, self.player1_pos - 1, 0, self.player2_pos - 1, 0, 3)
        self.move(True, 9, self.player1_pos - 1, 0, self.player2_pos - 1, 0, 1)


def parse_input(input: str) -> (int, int):
    player1, player2 = input.strip().split("\n")
    return int(player1[-1]), int(player2[-1])


with open("2021/day-21/example.txt") as f:
    player1, player2 = parse_input(f.read())
    game = DiracDiceGame(player1, player2, 100)
    loser_score, rolled_dices = game.play(1000)
    assert 739785 == loser_score * rolled_dices
    quantum_game = DiracDiceQuantumGame(player1, player2)
    quantum_game.play()
    assert 444356092776315 == max(quantum_game.wins)

with open("2021/day-21/input.txt") as f:
    player1, player2 = parse_input(f.read())
    game = DiracDiceGame(player1, player2, 100)
    loser_score, rolled_dices = game.play(1000)
    print("Part 1: The loser score multiplied by the rolled dices is:", loser_score * rolled_dices)
    quantum_game = DiracDiceQuantumGame(player1, player2)
    quantum_game.play()
    print("Part 2: The wins of the player that wins most is:", max(quantum_game.wins))
