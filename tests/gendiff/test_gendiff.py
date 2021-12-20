from gendiff.formatter.render import STYLE_STYLISH
from gendiff.generate_diff import generate_diff
from tests.file_loader import read_fixtures_file


def test_gendiff():
    result = read_fixtures_file('not_plain_test1_result.txt')
    diff = generate_diff('tests/fixtures/not_plain_test1_example1.json',
                         'tests/fixtures/not_plain_test1_example2.json', STYLE_STYLISH)

    assert diff == result
