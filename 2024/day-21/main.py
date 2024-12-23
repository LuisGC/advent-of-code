from functools import lru_cache
import sys
sys.path.insert(0, './')
from utils import profiler

class Keyboard:
    Vector = tuple[int, int]
    KeyPad = dict[str, Vector]

    moves = {
        "^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)
    }

    num_pad: KeyPad = {
        "7": (0, 0), "8": (1, 0), "9": (2, 0),
        "4": (0, 1), "5": (1, 1), "6": (2, 1),
        "1": (0, 2), "2": (1, 2), "3": (2, 2),
                     "0": (1, 3), "A": (2, 3)
    }

    dir_pad: KeyPad = {
                     "^": (1, 0), "A": (2, 0),
        "<": (0, 1), "v": (1, 1), ">": (2, 1),
    }

def getSequencesToPressKey(prev_key: str, next_key: str, key_pad: Keyboard.KeyPad) -> list[str]:
    if prev_key == next_key:
        return ["A"]

    start, target = key_pad[prev_key], key_pad[next_key]
    queue = [(start, "", [start])]
    sequences = []

    while len(queue) > 0:
        node, sequence, path = queue.pop(0)
        for move_symbol, (dx, dy) in Keyboard.moves.items():
            nex_node = (node[0] + dx, node[1] + dy)
            seq_with_move = sequence + move_symbol
            if nex_node == target:
                if not sequences or len(sequences[0]) == len(seq_with_move):
                    sequences.append(seq_with_move)
            elif nex_node in key_pad.values() and nex_node not in path:
                queue.append((nex_node, seq_with_move, path + [nex_node]))

    return [sequence + "A" for sequence in sequences]

@lru_cache(maxsize=None)
def getLengthOfPressing(code: str, robot_depth: int) -> int:
    if robot_depth == 1:
        return len(code)
    
    key_pad = Keyboard.num_pad if any(map(str.isdigit, code)) else Keyboard.dir_pad

    length_of_pressing = 0
    for prev_key, next_key in zip("A" + code, code):
        shortest_paths = getSequencesToPressKey(prev_key, next_key, key_pad)
        length_of_pressing += min(getLengthOfPressing(sp, robot_depth - 1) for sp in shortest_paths)

    return length_of_pressing

def get_code_complexity(code: str, middle_robots) -> int:
    length_of_pressing = getLengthOfPressing(code, 1 + middle_robots + 1)

    return length_of_pressing * int(code[:-1])

@profiler
def sum_of_complexities(code: str, middle_robots: int = 2) -> int:
    return sum(get_code_complexity(code, middle_robots) for code in codes)


with open("2024/day-21/example.txt", encoding="utf-8") as f:
    codes = list(map(str, f.read().splitlines()))

    assert 126384 == sum_of_complexities(codes, middle_robots=2)

with open("2024/day-21/input.txt", encoding="utf-8") as f:
    codes = list(map(str, f.read().splitlines()))

    print(f"Part 1: Sum of complexities is {sum_of_complexities(codes, middle_robots=2)}")
    print(f"Part 2: Sum of complexities with 25 middle robots is {sum_of_complexities(codes, middle_robots=25)}")    