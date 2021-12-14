import json
from typing import List, Optional

import yaml


FORMAT_JSON = 'json'
FORMAT_YML = 'yml'
FORMAT_YAML = 'yaml'

STATUS_CHANGED = 'CHANGED'
STATUS_NOT_CHANGED = 'NOT_CHANGED'
STATUS_REMOVED = 'REMOVED'
STATUS_ADDED = 'ADDED'
STATUS_CHILDREN = 'CHILDREN'


def find_diff(text1: str, text2: str, file_format: str) -> List[dict]:
    if file_format == FORMAT_JSON:
        return find_diff_json(text1, text2)

    if file_format == FORMAT_YAML or file_format == FORMAT_YML:
        return find_diff_yaml(text1, text2)

    raise Exception("Unknown file extension")


def find_diff_json(text1, text2) -> List[dict]:
    json1 = json.loads(text1)
    json2 = json.loads(text2)
    return find_diff_dict(json1, json2)


def find_diff_yaml(text1, text2) -> List[dict]:
    data1 = yaml.load(text1, Loader=yaml.CLoader)
    data2 = yaml.load(text2, Loader=yaml.CLoader)
    return find_diff_dict(data1, data2)


def find_diff_dict(dict1, dict2) -> List[dict]:
    return find_diff_dict_recursive(dict1, dict2)


def find_diff_dict_recursive(data1, data2) -> List[dict]:
    all_keys = list(data1.keys())
    all_keys.extend(list(data2.keys()))
    keys = set(all_keys)

    diff = []
    for key in keys:
        if key in data1 and key not in data2:
            diff.append(difference_data(key, STATUS_REMOVED, old_value=data1[key]))
        elif key not in data1 and key in data2:
            diff.append(difference_data(key, STATUS_ADDED, value=data2[key]))
        elif type(data1[key]) == dict and type(data2[key]) == dict:
            child_diff = find_diff_dict_recursive(data1[key], data2[key])
            diff.append(difference_data(key, STATUS_CHILDREN, children=child_diff))
        elif data1[key] != data2[key]:
            diff.append(difference_data(key, STATUS_CHANGED, value=data2[key],
                                        old_value=data1[key]))
        else:
            diff.append(difference_data(key, STATUS_NOT_CHANGED, value=data1[key]))

    return diff


def difference_data(key: str, status: str, value=None, old_value=None, children: Optional[List] = None) -> dict:
    return {
        'key': key,
        'status': status,
        'old_value': old_value,
        'value': value,
        'children': children
    }
