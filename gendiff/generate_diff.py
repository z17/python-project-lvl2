from gendiff.differ import parser
from gendiff.formatter import render
from gendiff.differ.loader import get_file_data
from gendiff.differ import differ


def generate_diff(file_path1, file_path2, style=render.STYLE_STYLISH):
    text1, extension1 = get_file_data(file_path1)
    text2, extension2 = get_file_data(file_path2)

    if extension1 != extension2:
        raise Exception("Invalid file formats")

    data1, data2 = parser.parse(text1, text2, extension1)

    diff = differ.find_diff(data1, data2)

    return render.render(style, diff)
