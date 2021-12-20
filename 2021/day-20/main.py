from typing import List
import numpy as np

def parse_input(input: str) -> (str, dict):
    algorithm, input_image = input.split("\n\n")
    input_image = input_image.strip().split("\n")
    image = np.zeros([len(input_image), len(input_image[0])])

    for r in range(len(image)):
        for c in range(len(image[0])):
            image[r,c] = input_image[r][c] == "#"

    return algorithm, np.pad(image, 3)


def enhance(algorithm: str, image: dict) -> dict:
    enhanced_image = np.zeros([len(image) - 2, len(image[0]) - 2])
    for r in range(len(enhanced_image)):
        r_old = r + 1
        for c in range(len(enhanced_image[0])):
            c_old = c + 1
            bin_code = ''
            for y in range(r_old - 1, r_old + 2):
                for x in range(c_old - 1, c_old + 2):
                    bin_code += str(int(image[y][x]))

            enhanced_image[r, c] = 1 if algorithm[int(bin_code, 2)] == '#' else 0
    enhanced_image = np.pad(enhanced_image, 3, mode='edge')

    return enhanced_image


with open("2021/day-20/example.txt") as f:
    algorithm, image = parse_input(f.read())
    enhanced_image = enhance(algorithm, image)
    assert 24 == int(sum(sum(enhanced_image)))
    enhanced_image = enhance(algorithm, enhanced_image)
    assert 35 == int(sum(sum(enhanced_image)))
    for _ in range(48):
        enhanced_image = enhance(algorithm, enhanced_image)
    assert 3351 == int(sum(sum(enhanced_image)))

with open("2021/day-20/input.txt") as f:
    algorithm, image = parse_input(f.read())
    for _ in range(2):
        image = enhance(algorithm, image)
    print("Part 1: The amount of lit pixels is:", int(sum(sum(image))))
    for _ in range(48):
        image = enhance(algorithm, image)
    print("Part 2: The amout of lit pixels after 50 enhancements is:", int(sum(sum(image))))
