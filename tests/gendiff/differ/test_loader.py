from gendiff.differ.loader import clear_extension


def test_clear_extension():
    cleared1 = clear_extension('.json')
    assert cleared1 == 'json'

    cleared2 = clear_extension('YML')
    assert cleared2 == 'yml'
