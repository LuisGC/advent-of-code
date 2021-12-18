class Probe:
    x = 0
    y = 0
    max_y = 0

    def __init__(self, start_vel_x: int, start_vel_y: int, target_x1: int, target_x2: int, target_y1: int, target_y2: int):
        self.start_vel_x = start_vel_x
        self.start_vel_y = start_vel_y
        self.velocity_x = start_vel_x
        self.velocity_y = start_vel_y


        self.target_min_x = min(target_x1, target_x2)
        self.target_max_x = max(target_x1, target_x2)
        self.target_min_y = min(target_y1, target_y2)
        self.target_max_y = max(target_y1, target_y2)

    def __str__(self):
        string = 'Probe:\n'
        string += "Start Vel: " + str(self.start_vel_x) + " .. " + str(self.start_vel_y) + '\n'
        string += "Range in X: " + str(self.target_min_x) + " .. " + str(self.target_max_x) + '\n'
        string += "Range in Y: " + str(self.target_min_y) + " .. " + str(self.target_max_y) + '\n'
        return string


    def step(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.velocity_x < 0:
            self.velocity_x = self.velocity_x + 1
        elif self.velocity_x > 0:
            self.velocity_x = self.velocity_x - 1

        self.velocity_y = self.velocity_y - 1

        self.max_y = max(self.y, self.max_y)

    def is_on_track(self):
        if self.y < self.target_min_y and self.velocity_y <= 0:
            return False
        if self.x < self.target_min_x and self.velocity_x <= 0:
            return False
        if self.x > self.target_max_x:
            return False
        return True

    def is_in_target_area(self):
        return self.x in range(self.target_min_x, self.target_max_x + 1) and \
               self.y in range(self.target_min_y, self.target_max_y + 1)

def highest_trajectory(x1: int, x2: int, y1: int, y2: int) -> int:
    max_heigth_Probe = None
    initial_velocity_values = []

    for x in range(0, x2 + 1):
        for y in range(y1, 180): # 180 is the optimal number, started with higher ones
            probe = Probe(x, y, x1, x2, y1, y2)
            while probe.is_on_track():
                probe.step()
                if probe.is_in_target_area():
                    initial_velocity_values.append((probe.start_vel_x, probe.start_vel_y))
                    if max_heigth_Probe is None or max_heigth_Probe.max_y < probe.max_y:
                        max_heigth_Probe = probe
                        break

    return max_heigth_Probe.max_y, len(list(dict.fromkeys(initial_velocity_values)))


def parse_input(input: str) -> (int, int, int, int):
    range = input.split(": ")[1]
    range_x, range_y = range.split(", ")
    min_x = int(range_x.split("..")[0][2:])
    max_x = int(range_x.split("..")[1])
    min_y = int(range_y.split("..")[0][2:])
    max_y = int(range_y.split("..")[1])

    return min_x, max_x, min_y, max_y


with open("2021/day-17/example.txt") as f:
    x1, x2, y1, y2 = parse_input([line.strip() for line in f][0])
    highest, count = highest_trajectory(x1, x2, y1, y2)
    assert 45 == highest
    assert 112 == count

with open("2021/day-17/input.txt") as f:
    x1, x2, y1, y2 = parse_input([line.strip() for line in f][0])
    highest, count = highest_trajectory(x1, x2, y1, y2)
    print("Part 1: Highest height is:", highest)
    print("Part 2: Amount of distinct initial velocity values is:", count)
