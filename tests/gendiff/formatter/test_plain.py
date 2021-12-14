from gendiff.differ.differ import STATUS_ADDED, STATUS_REMOVED, STATUS_CHANGED, STATUS_CHILDREN, STATUS_NOT_CHANGED, \
    difference_data
from gendiff.formatter.plain import render_plain
from tests.functions import load_file


def test_render_plain():
    diff = [
        difference_data('key1', STATUS_ADDED, False),
        difference_data('key2', STATUS_REMOVED, False),
        difference_data('key3', STATUS_CHANGED, None, 5),
        difference_data('common', STATUS_CHILDREN, children=[
            difference_data('complex', STATUS_ADDED, {'hello': 5}),
            difference_data('key', STATUS_ADDED, True),
            difference_data('removed_complex', STATUS_CHANGED, value='skip', old_value={'complex': True}),
        ]),
        difference_data('key4', STATUS_NOT_CHANGED, 15),
    ]

    output = render_plain(diff)

    expected = load_file('tests/fixtures/render_plain_result1.txt')

    assert output == expected
