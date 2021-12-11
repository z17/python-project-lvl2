from gendiff.differ.Difference import Difference
from gendiff.differ.differ import STATUS_ADDED, STATUS_REMOVED, STATUS_CHANGED, STATUS_CHILDREN, STATUS_NOT_CHANGED
from gendiff.formatter.plain import render_plain
from tests.functions import load_file


def test_render_plain():
    diff = [
        Difference('key1', STATUS_ADDED, False),
        Difference('key2', STATUS_REMOVED, False),
        Difference('key3', STATUS_CHANGED, None, 5),
        Difference('common', STATUS_CHILDREN, children=[
            Difference('complex', STATUS_ADDED, {'hello': 5}),
            Difference('key', STATUS_ADDED, True),
            Difference('removed_complex', STATUS_CHANGED, 'skip', {'complex': True}),
        ]),
        Difference('key4', STATUS_NOT_CHANGED, 15),
    ]

    output = render_plain(diff)

    expected = load_file('tests/fixtures/render_plain_result1.txt')

    assert output == expected
