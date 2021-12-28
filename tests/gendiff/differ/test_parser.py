from gendiff.differ.parser import parse
from gendiff.differ.differ import FORMAT_JSON, FORMAT_YAML


def test_parse_json():
    text = '{"name": {"name1": 5}}'
    data = parse(text, FORMAT_JSON)

    assert data['name']['name1'] == 5


def test_parse_yaml():
    text = '''
name:
    name1: 5
    '''
    data = parse(text, FORMAT_YAML)

    assert data['name']['name1'] == 5
