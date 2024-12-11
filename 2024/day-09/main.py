from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Self

def sum_range(start: int, end: int) -> int:
    small = (start - 1) * start //2
    big = end * (end + 1) // 2
    return big - small

@dataclass(slots=True)
class File:
    id: int
    size: int

@dataclass(slots=True)
class Block:
    files: deque[File]
    remaining: int

@dataclass(slots=True)
class Disk:
    blocks: Sequence[Block]

    def compact(self) -> None:
        i = 0
        j = len(self.blocks) - 1

        while i<j:
            first_block = self.blocks[i]
            last_block = self.blocks[j]

            if first_block.remaining == 0:
                i += 1
                continue

            if not last_block.files:
                j -= 1
                continue

            last_file_size = last_block.files[-1].size

            if last_file_size <= first_block.remaining:
                first_block.files.append(last_block.files.pop())
                first_block.remaining -= last_file_size
                last_block.remaining += last_file_size
            else:
                first_block.files.append(
                    File(id=last_block.files[-1].id, size=first_block.remaining)
                )
                last_block.files[-1].size -= first_block.remaining
                last_block.remaining += first_block.remaining
                first_block.remaining = 0

    def checksum(self) -> int:
        res = 0
        file_start = 0
        for block in self.blocks:
            for file in block.files:
                file_end = file_start + file.size - 1
                res += sum_range(file_start, file_end) * file.id
                file_start += file.size
            file_start += block.remaining
       
        return res
    
    @classmethod
    def from_str(cls: Self, seq: Sequence[int]) -> Self:
        blocks: list[Block] = []
        size = len(seq)
        for i in range (0, size, 2):
            remaining = seq[i + 1] if i+1 < size else 0
            blocks.append(
                Block(
                    files=deque([File(id= i//2, size=seq[i])]),
                    remaining=remaining,
                )
            )
        return cls(blocks)


with open("2024/day-09/example.txt", encoding="utf-8") as f:
    input = f.read().rstrip()
    disk = Disk.from_str(list(map(int, input)))
    disk.compact()
    assert 1928 == disk.checksum()

with open("2024/day-09/input.txt", encoding="utf-8") as f:
    input = f.read().rstrip()
    disk = Disk.from_str(list(map(int, input)))
    disk.compact()
    print(f"Part 1: Disk checksum is {disk.checksum()}")
#    print(f"Part 2: Amount of rocks after 75 blinks is {stones_produced(rocks, 75)}")
