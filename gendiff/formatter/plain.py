from typing import List

from gendiff.differ.differ import TYPE_ADDED, TYPE_REMOVED, TYPE_CHANGED, TYPE_CHILDREN

PLAIN_LINE_TEMPLATE_ADDED = "Property '{key}' was added with value: {value}"
PLAIN_LINE_TEMPLATE_REMOVED = "Property '{key}' was removed"
PLAIN_LINE_TEMPLATE_UPDATED = "Property '{key}' was updated. From {old_value} to {new_value}"


def render_plain(diff: List[dict]) -> str:
    lines = render_plain_recursive(diff)
    return "\n".join(lines)


def render_plain_recursive(diff: List[dict], key_prefix='') -> List[str]:
    lines = []
    diff.sort(key=lambda a: a['key'])

    for diff_line in diff:
        line_type = diff_line['type']
        key = f'{key_prefix}{diff_line["key"]}'

        if line_type == TYPE_ADDED:
            value = format_value(diff_line['value'])
            lines.append(PLAIN_LINE_TEMPLATE_ADDED.format(key=key, value=value))
        if line_type == TYPE_REMOVED:
            lines.append(PLAIN_LINE_TEMPLATE_REMOVED.format(key=key))
        if line_type == TYPE_CHANGED:
            old_value = format_value(diff_line['old_value'])
            new_value = format_value(diff_line['value'])
            lines.append(
                PLAIN_LINE_TEMPLATE_UPDATED.format(key=key, old_value=old_value, new_value=new_value))
        if line_type == TYPE_CHILDREN:
            lines.extend(render_plain_recursive(diff_line['children'], f'{key}.'))

    return lines


def format_value(value) -> str:
    if type(value) == dict:
        return '[complex value]'

    if type(value) == str:
        return f"'{value}'"

    if type(value) == bool:
        return str(value).lower()

    if value is None:
        return 'null'

    return str(value)
