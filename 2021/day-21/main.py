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


def parse_input(input: str) -> (int, int):
    player1, player2 = input.strip().split("\n")
    return int(player1[-1]), int(player2[-1])


with open("2021/day-21/example.txt") as f:
    player1, player2 = parse_input(f.read())
    game = DiracDiceGame(player1, player2, 100)
    loser_score, rolled_dices = game.play(1000)
    assert 739785 == loser_score * rolled_dices

with open("2021/day-21/input.txt") as f:
    player1, player2 = parse_input(f.read())
    game = DiracDiceGame(player1, player2, 100)
    loser_score, rolled_dices = game.play(1000)
    print("Part 1: The loser score multiplied by the rolled dices is:", loser_score * rolled_dices)
#     print("Part 2: The amout of lit pixels after 50 enhancements is:", int(sum(sum(image))))
