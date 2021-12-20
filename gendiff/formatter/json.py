import json
from typing import List

from gendiff.differ.differ import TYPE_ADDED, TYPE_REMOVED, TYPE_CHANGED, TYPE_CHILDREN, TYPE_NOT_CHANGED


def render_json(diff: List[dict]) -> str:
    return json.dumps(convert_to_object(diff))


def convert_to_object(diff: List[dict]):
    lines = []
    for diff_line in diff:
        value = {
            'key': diff_line['key'],
            'status': diff_line['status']
        }

        if diff_line['status'] == TYPE_ADDED:
            value['value'] = diff_line['value']
        elif diff_line['status'] == TYPE_REMOVED:
            value['value'] = diff_line['old_value']
        elif diff_line['status'] == TYPE_CHANGED:
            value['old_value'] = diff_line['old_value']
            value['new_value'] = diff_line['value']
        elif diff_line['status'] == TYPE_NOT_CHANGED:
            value['value'] = diff_line['value']
        elif diff_line['status'] == TYPE_CHILDREN:
            value['children'] = convert_to_object(diff_line['children'])

        lines.append(value)

    return lines
