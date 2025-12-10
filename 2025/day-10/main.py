import re
import z3
from collections import deque

class Machine:
    def __init__(self, config: str):
        end_state = config.split(" ")[0][1:-1]
        self.end_state = tuple(c == "#" for c in end_state)
        buttons = re.findall(r"\((?:\d+,?)+\)", config)
        self.buttons = tuple([int(x) for x in re.findall(r"-?\d+", s)] for s in buttons)
        joltage = re.findall(r"{(?:\d+,?)+}", config)[0][1:-1].split(",")
        self.joltage = tuple(int(x) for x in joltage)

    def fewest_button_presses_for_light(self) -> int:
        initial_state = tuple([False] * len(self.end_state))
        seen = {initial_state}
        queue = deque([(initial_state, 0)])

        while len(queue) > 0:
            state, presses = queue.popleft()

            if state == self.end_state:
                return presses

            for button in self.buttons:
                new_state = list(state)

                for index in button:
                    if 0 <= index < len(new_state):
                        new_state[index] = not new_state[index]

                new_state_tuple = tuple(new_state)

                if new_state_tuple not in seen:
                    seen.add(new_state_tuple)
                    queue.append((new_state_tuple, presses + 1))

        return -1  # Should never reach here if a solution exists
    
    def fewest_button_presses_for_joltage(self) -> int:
        presses = [z3.Int(f"press_{i}") for i in range(len(self.buttons))]
        s = z3.Optimize()
        for press in presses:
            s.add(press >= 0)

        for i, jolt_level in enumerate(self.joltage):
            usable_presses = [
                presses[j] for j, button in enumerate(self.buttons) if i in button
            ]
            s.add(sum(usable_presses) == jolt_level)
        s.minimize(sum(presses))
        s.check()
        model = s.model()

        return sum(model[press].as_long() for press in presses)

def fewest_button_presses(lines: list[str]) -> tuple[int, int]:
    fewest_for_light = fewest_for_joltage = 0

    for line in lines:
        m = Machine(line)
        fewest_for_light += m.fewest_button_presses_for_light()
        fewest_for_joltage += m.fewest_button_presses_for_joltage()

    return fewest_for_light, fewest_for_joltage

with open("2025/day-10/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    fewest_for_light, fewest_for_joltage = fewest_button_presses(input_lines)
    assert 7 == fewest_for_light
    assert 33 == fewest_for_joltage

with open("2025/day-10/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    fewest_for_light, fewest_for_joltage = fewest_button_presses(input_lines)
    print(f"Part 1: The fewest button presses for light is {fewest_for_light}")
    print(f"Part 2: The fewest button presses for joltage is {fewest_for_joltage}")
