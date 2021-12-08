from typing import List

from gendiff.differ.differ import STATUS_CHANGED, STATUS_ADDED, \
    STATUS_NOT_CHANGED, STATUS_REMOVED, STATUS_CHILDREN

TEMPLATE_VALUE = '{spaces}{status} {key}: {value}'
TEMPLATE_DICT_OPEN = '{spaces}{status} {key}: {{'
TEMPLATE_DICT_CLOSE = '{spaces}}}'

STATUS_MAP = {
    STATUS_ADDED: '+',
    STATUS_REMOVED: '-',
    STATUS_NOT_CHANGED: ' ',
}


def stylish(diff: List):
    lines = ['{']
    lines.extend(stylish_recursive(diff))
    lines.append('}')
    return "\n".join(lines)


def stylish_format_value(key, value, status, level):
    spaces = get_spaces(level)
    if type(value) == dict:
        lines = [
            TEMPLATE_DICT_OPEN.format(spaces=spaces, status=status, key=key)]
        for key in value:
            lines.append(stylish_format_value(key, value[key], ' ', level + 1))

        lines.append(TEMPLATE_DICT_CLOSE.format(spaces=spaces))
        return "\n".join(lines)
    else:
        return TEMPLATE_VALUE.format(spaces=spaces, status=status,
                                     key=key,
                                     value=value)


def get_spaces(level):
    return ' ' * 2 * level


def stylish_recursive(diff: List, level=1):
    diff_lines = []
    for diff_line in diff:
        status = diff_line.status
        key = diff_line.key
        if status == STATUS_ADDED:
            diff_lines.append(
                stylish_format_value(key, diff_line.value, '+', level)
            )
        elif status == STATUS_REMOVED:
            diff_lines.append(
                stylish_format_value(key, diff_line.old_value, '-', level)
            )
        elif status == STATUS_CHANGED:
            diff_lines.append(
                stylish_format_value(key, diff_line.old_value, '-', level)
            )
            diff_lines.append(
                stylish_format_value(key, diff_line.value, '+', level)
            )
        elif status == STATUS_NOT_CHANGED:
            diff_lines.append(
                stylish_format_value(key, diff_line.value, ' ', level)
            )
        elif status == STATUS_CHILDREN:
            diff_lines.extend(
                stylish_recursive(diff_line.children, level+1)
            )

    return diff_lines


def stylish_recursive2(diff: List, level=1, key=None, key_status=None):
    spaces = ' ' * 2 * level
    spaces_brackets = ' ' * (2 * (level - 1))
    diff_lines = []
    if level == 1:
        diff_lines.append('{')
    else:
        if key_status == STATUS_CHANGED:
            diff_lines.append(
                TEMPLATE_DICT_OPEN.format(spaces_brackets,
                                          STATUS_MAP[STATUS_REMOVED], key))
            diff_lines.append(
                TEMPLATE_DICT_OPEN.format(spaces_brackets,
                                          STATUS_MAP[STATUS_ADDED],
                                          key))
        else:
            diff_lines.append(
                TEMPLATE_DICT_OPEN.format(spaces_brackets,
                                          STATUS_MAP[key_status],
                                          key))

    for diff_key in diff:
        status = diff_key.status
        key = diff_key.key

        if diff_key.children:
            diff_lines.append(
                stylish_recursive(diff_key.children, level + 1, key, status))
        else:

            if status == STATUS_CHANGED:
                diff_lines.append(
                    TEMPLATE_VALUE.format(spaces, STATUS_MAP[STATUS_REMOVED],
                                          key,
                                          diff_key.old_value))
                diff_lines.append(
                    TEMPLATE_VALUE.format(spaces, STATUS_MAP[STATUS_ADDED], key,
                                          diff_key.value))
            elif status == STATUS_REMOVED:
                diff_lines.append(
                    TEMPLATE_VALUE.format(spaces, STATUS_MAP[status], key,
                                          diff_key.old_value))
            elif status == STATUS_ADDED:
                diff_lines.append(
                    TEMPLATE_VALUE.format(spaces, STATUS_MAP[status], key,
                                          diff_key.value))
            elif status == STATUS_NOT_CHANGED:
                diff_lines.append(
                    TEMPLATE_VALUE.format(spaces, STATUS_MAP[status], key,
                                          diff_key.value))

    diff_lines.append(TEMPLATE_DICT_CLOSE.format(spaces_brackets))
    return "\n".join(diff_lines)
