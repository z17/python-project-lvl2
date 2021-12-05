from gendiff.generate_diff import generate_diff
from tests.functions import load_file


def test_gendiff():
    result = load_file('tests/fixtures/not_plain_test1_result.txt')
    diff = generate_diff('tests/fixtures/not_plain_test1_example1.json',
                         'tests/fixtures/not_plain_test1_example2.json')

    #todo: test
    # assert diff == result
