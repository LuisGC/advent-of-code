def check_validity(list):
    return 0;


with open("day-04/example.txt") as f:
    document_list = f.readlines()
    assert 7 == check_validity(document_list)
