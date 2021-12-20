from gendiff.differ.differ import TYPE_ADDED, TYPE_REMOVED, TYPE_CHANGED, TYPE_CHILDREN, TYPE_NOT_CHANGED, \
    difference_data
from gendiff.formatter.plain import render_plain
from tests.file_loader import read_fixtures_file


def test_render_plain():
    diff = [
        difference_data('key1', TYPE_ADDED, False),
        difference_data('key2', TYPE_REMOVED, False),
        difference_data('key3', TYPE_CHANGED, None, 5),
        difference_data('common', TYPE_CHILDREN, children=[
            difference_data('complex', TYPE_ADDED, {'hello': 5}),
            difference_data('key', TYPE_ADDED, True),
            difference_data('removed_complex', TYPE_CHANGED, value='skip', old_value={'complex': True}),
        ]),
        difference_data('key4', TYPE_NOT_CHANGED, 15),
    ]

    output = render_plain(diff)

    expected = read_fixtures_file('render_plain_result1.txt')

    assert output == expected
