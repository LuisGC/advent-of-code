def find_handshake(card_private_key: int, door_private_key: int) -> int:
    subject_number = 1
    door_public_key, card_public_key = 1, 1

    while True:
        subject_number = (subject_number * 7) % 20201227
        door_public_key = (door_public_key * card_private_key) % 20201227
        card_public_key = (card_public_key * door_private_key) % 20201227
        if subject_number == card_private_key:
            return card_public_key
        if subject_number == door_private_key:
            return door_public_key


assert 14897079 == find_handshake(5764801, 17807724)

print("Part 1: The handshake is: ", find_handshake(335121, 363891))
