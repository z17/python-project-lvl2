import json

import yaml

from tests.file_loader import read_fixtures_file
from gendiff.differ.differ import find_diff, TYPE_CHANGED, TYPE_REMOVED


def test_json_check_plain():
    file1 = read_fixtures_file('file1.json')
    file2 = read_fixtures_file('file2.json')
    data1 = json.loads(file1)
    data2 = json.loads(file2)

    diff = find_diff(data1, data2)

    has_timeout = list(filter(lambda x: x['key'] == 'timeout', diff))
    assert has_timeout[0]['status'] == TYPE_CHANGED
    assert has_timeout[0]['value'] == 20
    assert has_timeout[0]['old_value'] == 50

    has_timeout = list(filter(lambda x: x['key'] == 'follow', diff))
    assert has_timeout[0]['status'] == TYPE_REMOVED
    assert not has_timeout[0]['value']


def test_yaml_check_plain():
    file1 = read_fixtures_file('yaml_test1_file1.yml')
    file2 = read_fixtures_file('yaml_test1_file2.yml')
    data1 = yaml.load(file1, Loader=yaml.CLoader)
    data2 = yaml.load(file2, Loader=yaml.CLoader)

    diff = find_diff(data1, data2)

    has_timeout = list(filter(lambda x: x['key'] == 'timeout', diff))
    assert has_timeout[0]['status'] == TYPE_CHANGED
    assert has_timeout[0]['value'] == 20
    assert has_timeout[0]['old_value'] == 50

    has_timeout = list(filter(lambda x: x['key'] == 'follow', diff))
    assert has_timeout[0]['status'] == TYPE_REMOVED
    assert not has_timeout[0]['value']


def test_json_check_not_plain():
    file1 = read_fixtures_file('not_plain_test1_example1.json')
    file2 = read_fixtures_file('not_plain_test1_example2.json')
    data1 = json.loads(file1)
    data2 = json.loads(file2)

    diff = find_diff(data1, data2)

    common = list(filter(lambda x: x['key'] == 'common', diff))[0]
    setting2 = list(filter(lambda x: x['key'] == 'setting2', common['children']))[0]
    setting3 = list(filter(lambda x: x['key'] == 'setting3', common['children']))[0]

    assert setting2['status'] == TYPE_REMOVED
    assert setting2['old_value'] == 200

    assert setting3['status'] == TYPE_CHANGED
    assert setting3['value'] is None
