import json

from gendiff.formatter.json import render_json
from gendiff.differ.differ import STATUS_ADDED, STATUS_REMOVED, STATUS_CHANGED, STATUS_CHILDREN, STATUS_NOT_CHANGED, \
    difference_data


def test_render_plain():
    diff = [
        difference_data('key1', STATUS_ADDED, False),
        difference_data('key2', STATUS_REMOVED, old_value=False),
        difference_data('key3', STATUS_CHANGED, None, 5),
        difference_data('key4', STATUS_CHANGED, value='str', old_value={5: 'a'}),
        difference_data('dict_key', STATUS_CHILDREN, children=[
            difference_data('key', STATUS_ADDED, True),
        ]),
        difference_data('key4', STATUS_NOT_CHANGED, 15),
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
