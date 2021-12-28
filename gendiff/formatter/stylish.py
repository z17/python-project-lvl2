from typing import List

from gendiff.differ.differ import TYPE_CHANGED, TYPE_ADDED, \
    TYPE_NOT_CHANGED, TYPE_REMOVED, TYPE_CHILDREN

TEMPLATE_VALUE = '{spaces}{sign} {key}: {value}'
TEMPLATE_DICT_OPEN = '{spaces}{sign} {key}: {{'
TEMPLATE_DICT_CLOSE = '  {spaces}}}'

TYPE_MAP = {
    TYPE_ADDED: '+',
    TYPE_REMOVED: '-',
    TYPE_NOT_CHANGED: ' ',
}


def render_stylish(diff: List[dict]):
    return "\n".join(get_stylish_lines(diff))


def format_value(key, value, sign, level):
    spaces = get_spaces(level)
    if type(value) == dict:
        lines = [
            TEMPLATE_DICT_OPEN.format(spaces=spaces, sign=sign, key=key)]
        for key in value:
            lines.append(format_value(key, value[key], ' ', level + 1))

        lines.append(TEMPLATE_DICT_CLOSE.format(spaces=spaces))
        return "\n".join(lines)
    else:
        if type(value) == bool:
            val_string = str(value).lower()
        elif value is None:
            val_string = 'null'
        else:
            val_string = str(value)

        return TEMPLATE_VALUE.format(spaces=spaces, sign=sign,
                                     key=key,
                                     value=val_string)


def get_spaces(level):
    return ' ' * (4 * level - 2)


def get_stylish_lines(diff: List[dict], level=1):
    diff_lines = []
    if level == 1:
        diff_lines.append('{')

    diff.sort(key=lambda a: a['key'])
    for diff_line in diff:
        line_type = diff_line['type']
        key = diff_line['key']
        if line_type == TYPE_ADDED:
            diff_lines.append(
                format_value(key, diff_line['value'], '+', level)
            )
        elif line_type == TYPE_REMOVED:
            diff_lines.append(
                format_value(key, diff_line['old_value'], '-', level)
            )
        elif line_type == TYPE_CHANGED:
            diff_lines.append(
                format_value(key, diff_line['old_value'], '-', level)
            )
            diff_lines.append(
                format_value(key, diff_line['value'], '+', level)
            )
        elif line_type == TYPE_NOT_CHANGED:
            diff_lines.append(
                format_value(key, diff_line['value'], ' ', level)
            )
        elif line_type == TYPE_CHILDREN:
            spaces = get_spaces(level)
            diff_lines.append(
                TEMPLATE_DICT_OPEN.format(spaces=spaces, sign=' ', key=key))
            diff_lines.extend(
                get_stylish_lines(diff_line['children'], level + 1)
            )
            diff_lines.append(TEMPLATE_DICT_CLOSE.format(spaces=spaces))

    if level == 1:
        diff_lines.append('}')

    return diff_lines
