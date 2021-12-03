
from gendiff.differ.differ import find_diff, FORMAT_JSON, FORMAT_YAML


def test_json_check():
    file1 = load_file('tests/fixtures/file1.json')
    file2 = load_file('tests/fixtures/file2.json')

    diff = find_diff(file1, file2, FORMAT_JSON)

    assert ('-', 'timeout', 50) in diff
    assert ('+', 'timeout', 20) in diff
    assert ('-', 'follow', False) in diff


def test_yaml_check():
    file1 = load_file('tests/fixtures/yaml_test1_file1.yml')
    file2 = load_file('tests/fixtures/yaml_test1_file2.yml')

    diff = find_diff(file1, file2, FORMAT_YAML)

    assert ('-', 'timeout', 50) in diff
    assert ('+', 'timeout', 20) in diff
    assert ('-', 'follow', False) in diff


def load_file(name):
    with open(name, 'r') as file:
        return file.read()
