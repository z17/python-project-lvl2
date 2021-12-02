import json

from gendiff.differ.differ import find_diff


def test_one():
    file1 = load_file('tests/data/file1.json')
    file2 = load_file('tests/data/file2.json')

    diff = find_diff(file1, file2)
    print(diff)

    assert ('-', 'timeout', 50) in diff
    assert ('+', 'timeout', 20) in diff
    assert ('-', 'follow', False) in diff


def load_file(name):
    with open(name, 'r') as file:
        return json.load(file)
