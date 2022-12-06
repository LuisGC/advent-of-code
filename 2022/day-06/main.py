def first_marker(packet: str, size: int) -> int:

    return 1+next(i for i in range(size, len(packet)) if len(set(packet[i:i-size:-1])) == size)

with open("2022/day-06/input.txt", encoding="utf-8") as f:
    assert 7 == first_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4)
    assert 5 == first_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 4)
    assert 6 == first_marker("nppdvjthqldpwncqszvftbrmjlhg", 4)
    assert 10 == first_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4)
    assert 11 == first_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4)

    lines = f.readlines()
    print("Part 1: First marker with 4 characters is:", first_marker(lines[0], 4))

    # Part 2
    assert 19 == first_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14)
    assert 23 == first_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 14)
    assert 23 == first_marker("nppdvjthqldpwncqszvftbrmjlhg", 14)
    assert 29 == first_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14)
    assert 26 == first_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14)

    print("Part 2: First marker with 14 characters is:", first_marker(lines[0], 14))
