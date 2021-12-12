from gendiff.formatter.render import render, STYLE_STYLISH
from gendiff.differ.loader import get_file_data
from gendiff.differ.differ import find_diff


def generate_diff(file_path1, file_path2, style=STYLE_STYLISH):
    text1, extension1 = get_file_data(file_path1)
    text2, extension2 = get_file_data(file_path2)

    if extension1 != extension2:
        raise Exception("Invalid file formats")

    diff = find_diff(text1, text2, extension1)

    return render(style, diff)
