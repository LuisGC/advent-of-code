from typing import List

class Brick:
    def __init__(self, start, end):
        self.start, self.end = sorted([start, end])
        self.supports = []
        self.supported_by = []
    def __repr__(self):
        return f"Brick({self.start}, {self.end})"
    def intersect(self, other: "Brick"):
        sx1, sy1, sz1 = self.start
        ex1, ey1, ez1 = self.end
        sx2, sy2, sz2 = other.start
        ex2, ey2, ez2 = other.end
        return (sx1 <= ex2 and sx2 <= ex1 and
                sy1 <= ey2 and sy2 <= ey1 and
                sz1 <= ez2 and sz2 <= ez1)
    def key_z(self):
        return self.start[2]
    def move_down(self):
        return Brick((self.start[0], self.start[1], self.start[2]-1), (self.end[0], self.end[1], self.end[2]-1))
    def __iter__(self):
        return ((x, y, z)
                for x in range(self.start[0], self.end[0] + 1)
                for y in range(self.start[1], self.end[1] + 1)
                for z in range(self.start[2], self.end[2] + 1))
    def __hash__(self):
        return hash((self.start, self.end))

def parse_input(input_lines: List[str]) -> List[Brick]:
    bricks = []
    for line in input_lines:
        start, end = line.split("~")
        brick = Brick(tuple(map(int,start.split(','))),tuple(map(int,end.split(','))))
        bricks.append(brick)
    bricks.sort(key=Brick.key_z)
    return bricks

def settle_bricks(bricks: List[Brick]) -> int:
    for i in range(len(bricks)):
        while True:
            brick = bricks[i]
            new_brick = brick.move_down()
            if new_brick.start[2] <= 0:
                break
            for j, other in enumerate(bricks):
                if i == j:
                    continue
                if new_brick.intersect(other):
                    break
            else:
                bricks[i] = new_brick
                continue
            break

    bricks.sort(key=Brick.key_z)

    for brick in bricks:
        dropped_brick = brick.move_down()
        for other in bricks:
            if brick is other:
                continue
            if dropped_brick.intersect(other):
                other.supports.append(brick)
                brick.supported_by.append(other)

    return sum(all(len(top.supported_by)>1 for top in brick.supports) for brick in bricks)


with open("2023/day-22/example.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    bricks = parse_input(input_lines)
    
    assert 5 == settle_bricks(bricks)

with open("2023/day-22/input.txt", encoding="utf-8") as f:
    input_lines = [line.strip() for line in f.readlines()]
    bricks = parse_input(input_lines)
    
    print("Part 1: The amount of bricks that can be removed is ", settle_bricks(bricks))
    