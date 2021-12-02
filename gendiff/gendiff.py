from gendiff.differ.loader import get_data
from gendiff.differ.differ import find_diff

CONST_TEMPLATE = '  {} {} {}'


def generate_diff(file_path1, file_path2):
    json1 = get_data(file_path1)
    json2 = get_data(file_path2)

    diff = find_diff(json1, json2)

    diff_lines = ['{']
    for diff_line in diff:
        sign, key, value = diff_line
        diff_lines.append(CONST_TEMPLATE.format(sign, key, value))
    diff_lines.append('}')

    return "\n".join(diff_lines)
