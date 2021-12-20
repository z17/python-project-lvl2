from gendiff.differ.loader import standardize_extension


def test_standardize_extension():
    cleared1 = standardize_extension('.json')
    assert cleared1 == 'json'

    cleared2 = standardize_extension('YML')
    assert cleared2 == 'yml'
