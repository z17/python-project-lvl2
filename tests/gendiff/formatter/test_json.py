import json

from gendiff.formatter.json import render_json
from gendiff.differ.Difference import Difference
from gendiff.differ.differ import STATUS_ADDED, STATUS_REMOVED, STATUS_CHANGED, STATUS_CHILDREN, STATUS_NOT_CHANGED


def test_render_plain():
    diff = [
        Difference('key1', STATUS_ADDED, False),
        Difference('key2', STATUS_REMOVED, old_value=False),
        Difference('key3', STATUS_CHANGED, None, 5),
        Difference('key4', STATUS_CHANGED, 'str', {5: 'a'}),
        Difference('dict_key', STATUS_CHILDREN, children=[
            Difference('key', STATUS_ADDED, True),
        ]),
        Difference('key4', STATUS_NOT_CHANGED, 15),
    ]

    output = render_json(diff)

    parsed_output = json.loads(output)

    key1_diff = list(filter(lambda x: x['key'] == 'key1', parsed_output))[0]
    key2_diff = list(filter(lambda x: x['key'] == 'key2', parsed_output))[0]
    key4_diff = list(filter(lambda x: x['key'] == 'key4', parsed_output))[0]
    dict_diff = list(filter(lambda x: x['key'] == 'dict_key', parsed_output))[0]

    assert key1_diff['key'] == 'key1'
    assert key1_diff['status'] == 'ADDED'

    assert key2_diff['key'] == 'key2'
    assert key2_diff['status'] == 'REMOVED'
    assert not key2_diff['value']

    assert key4_diff['key'] == 'key4'
    assert key4_diff['status'] == 'CHANGED'
    assert key4_diff['new_value'] == 'str'

    assert dict_diff['children'][0]['key'] == 'key'
