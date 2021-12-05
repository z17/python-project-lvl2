from typing import List

from gendiff.differ.differ import STATUS_CHANGED, STATUS_ADDED, \
    STATUS_NOT_CHANGED, STATUS_REMOVED

TEMPLATE_VALUE = '{}{} {}: {}'
TEMPLATE_DICT_OPEN = '{}{} {}: {{'
TEMPLATE_DICT_CLOSE = '{}}}'

STATUS_MAP = {
    STATUS_ADDED: '+',
    STATUS_REMOVED: '-',
    STATUS_NOT_CHANGED: ' ',
}


def stylish(diff: List):
    return stylish_recursive(diff)


def stylish_recursive(diff: List, level=1, key=None, key_status=None):
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
