from gendiff.differ.loader import get_file_data
from gendiff.differ.differ import find_diff

CONST_TEMPLATE = '  {} {} {}'


def generate_diff(file_path1, file_path2):
    text1, extension1 = get_file_data(file_path1)
    text2, extension2 = get_file_data(file_path2)

    if extension1 != extension2:
        raise Exception("Invalid file formats")

    diff = find_diff(text1, text2, extension1)

    diff_lines = ['{']
    for diff_line in diff:
        sign, key, value = diff_line
        diff_lines.append(CONST_TEMPLATE.format(sign, key, value))
    diff_lines.append('}')

    return "\n".join(diff_lines)
