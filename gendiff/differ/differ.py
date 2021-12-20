from typing import List, Optional

FORMAT_JSON = 'json'
FORMAT_YML = 'yml'
FORMAT_YAML = 'yaml'

TYPE_CHANGED = 'CHANGED'
TYPE_NOT_CHANGED = 'NOT_CHANGED'
TYPE_REMOVED = 'REMOVED'
TYPE_ADDED = 'ADDED'
TYPE_CHILDREN = 'CHILDREN'


def find_diff(data1, data2) -> List[dict]:
    all_keys = list(data1.keys())
    all_keys.extend(list(data2.keys()))
    keys = set(all_keys)

    diff = []
    for key in keys:
        if key in data1 and key not in data2:
            diff.append(difference_data(key, TYPE_REMOVED, old_value=data1[key]))
        elif key not in data1 and key in data2:
            diff.append(difference_data(key, TYPE_ADDED, value=data2[key]))
        elif type(data1[key]) == dict and type(data2[key]) == dict:
            child_diff = find_diff(data1[key], data2[key])
            diff.append(difference_data(key, TYPE_CHILDREN, children=child_diff))
        elif data1[key] != data2[key]:
            diff.append(difference_data(key, TYPE_CHANGED, value=data2[key],
                                        old_value=data1[key]))
        else:
            diff.append(difference_data(key, TYPE_NOT_CHANGED, value=data1[key]))

    return diff


def difference_data(key: str, status: str, value=None, old_value=None, children: Optional[List] = None) -> dict:
    return {
        'key': key,
        'status': status,
        'old_value': old_value,
        'value': value,
        'children': children
    }
