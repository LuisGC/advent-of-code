import re
from collections import deque

class Machine:
    def __init__(self, config: str):
        end_state = config.split(" ")[0][1:-1]
        self.end_state = tuple(c == "#" for c in end_state)
        buttons = re.findall(r"\((?:\d+,?)+\)", config)
        self.buttons = tuple([int(x) for x in re.findall(r"-?\d+", s)] for s in buttons)

    def fewest_button_presses(self) -> int:
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

def fewest_button_presses(lines: list[str]) -> int:
    fewest = 0

    for line in lines:
        m = Machine(line)
        fewest += m.fewest_button_presses()

    return fewest

with open("2025/day-10/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    assert 7 == fewest_button_presses(input_lines)

with open("2025/day-10/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]

    print(f"Part 1: The fewest button presses is {fewest_button_presses(input_lines)}")
