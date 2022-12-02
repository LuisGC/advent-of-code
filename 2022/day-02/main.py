from typing import List

def calculate_score(plays: List):
    score = 0
    wins = ['1 2', '2 3', '3 1']
    ties = ['1 1', '2 2', '3 3']

    score += 6 * len([line for line in plays if line in wins]) 
    score += 3 * len([line for line in plays if line in ties]) 
    score += sum([int(line[-1]) for line in plays])

    # print("Score: ", score)
    return score

def decrypt_plays(plays: List) -> List:

    strategy = []

    for play in plays:
        cheat_play = ""
        if play[-1] == "2": # Draw
            cheat_play = play[0]
        elif play[-1] == "1": # Lose
            if play[0] == "1":
                cheat_play = "3"
            elif play[0] == "2":
                cheat_play = "1"
            else:
                cheat_play = "2"
        else: # Win
            if play[0] == "1":
                cheat_play = "2"
            elif play[0] == "2":
                cheat_play = "3"
            else:
                cheat_play = "1"

        strategy.append(play[0] + play[1] + cheat_play)

    return strategy

def clean_input_lines(input_lines: List) -> List:
    clean_lines = [line.replace('X', 'A').replace('Y', 'B').replace('Z', 'C') for line in input_lines]
    return [line.replace('A', '1').replace('B', '2').replace('C', '3') for line in clean_lines]


with open("2022/day-02/example.txt") as f:
    input_lines = [line.strip() for line in f.readlines()]
    clean_plays = clean_input_lines(input_lines)
    assert 15 == calculate_score(clean_plays)

    cheat_plays = decrypt_plays(clean_plays)
    assert 12 == calculate_score(cheat_plays)

with open("2022/day-02/input.txt") as f:
    input_lines = [line.strip() for line in f.readlines()]
    clean_plays = clean_input_lines(input_lines)

    print("Part 1: Score is ", calculate_score(clean_plays))
    cheat_plays = decrypt_plays(clean_plays)
    calculate_score(cheat_plays)
    print("Part 2: Score applying strategy is ", calculate_score(cheat_plays))
