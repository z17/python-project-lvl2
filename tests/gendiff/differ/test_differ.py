from tests.functions import load_file
from gendiff.differ.differ import find_diff, FORMAT_JSON, FORMAT_YAML, \
    STATUS_CHANGED, STATUS_REMOVED


def test_json_check_plain():
    file1 = load_file('tests/fixtures/file1.json')
    file2 = load_file('tests/fixtures/file2.json')

    diff = find_diff(file1, file2, FORMAT_JSON)

    has_timeout = list(filter(lambda x: x['key'] == 'timeout', diff))
    assert has_timeout[0]['status'] == STATUS_CHANGED
    assert has_timeout[0]['value'] == 20
    assert has_timeout[0]['old_value'] == 50

    has_timeout = list(filter(lambda x: x['key'] == 'follow', diff))
    assert has_timeout[0]['status'] == STATUS_REMOVED
    assert not has_timeout[0]['value']


def test_yaml_check_plain():
    file1 = load_file('tests/fixtures/yaml_test1_file1.yml')
    file2 = load_file('tests/fixtures/yaml_test1_file2.yml')

    diff = find_diff(file1, file2, FORMAT_YAML)

    has_timeout = list(filter(lambda x: x['key'] == 'timeout', diff))
    assert has_timeout[0]['status'] == STATUS_CHANGED
    assert has_timeout[0]['value'] == 20
    assert has_timeout[0]['old_value'] == 50

    has_timeout = list(filter(lambda x: x['key'] == 'follow', diff))
    assert has_timeout[0]['status'] == STATUS_REMOVED
    assert not has_timeout[0]['value']


def test_json_check_not_plain():
    file1 = load_file('tests/fixtures/not_plain_test1_example1.json')
    file2 = load_file('tests/fixtures/not_plain_test1_example2.json')

    diff = find_diff(file1, file2, FORMAT_JSON)

    common = list(filter(lambda x: x['key'] == 'common', diff))[0]
    setting2 = list(filter(lambda x: x['key'] == 'setting2', common['children']))[0]
    setting3 = list(filter(lambda x: x['key'] == 'setting3', common['children']))[0]

    assert setting2['status'] == STATUS_REMOVED
    assert setting2['old_value'] == 200

    assert setting3['status'] == STATUS_CHANGED
    assert setting3['value'] is None
