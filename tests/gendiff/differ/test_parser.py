from gendiff.differ.parser import parse
from gendiff.differ.differ import FORMAT_JSON, FORMAT_YAML


def test_parse_json():
    text1 = '{"name":"value"}'
    text2 = '{"name": {"name1": 5}}'
    data1, data2 = parse(text1, text2, FORMAT_JSON)

    assert data1['name'] == 'value'
    assert data2['name']['name1'] == 5


def test_parse_yaml():
    text1 = '''
name: "value"
    '''
    text2 = '''
name: 
    name1: 5
    '''
    data1, data2 = parse(text1, text2, FORMAT_YAML)

    assert data1['name'] == 'value'
    assert data2['name']['name1'] == 5
