import json
import yaml

from gendiff.differ.Difference import Difference

FORMAT_JSON = 'json'
FORMAT_YML = 'yml'
FORMAT_YAML = 'yaml'

STATUS_CHANGED = 'CHANGED'
STATUS_NOT_CHANGED = 'NOT_CHANGED'
STATUS_REMOVED = 'REMOVED'
STATUS_ADDED = 'ADDED'


def find_diff(text1, text2, file_format):
    if file_format == FORMAT_JSON:
        return find_diff_json(text1, text2)

    if file_format == FORMAT_YAML or file_format == FORMAT_YML:
        return find_diff_yaml(text1, text2)

    raise Exception("Unknown file extension")


def find_diff_json(text1, text2):
    json1 = json.loads(text1)
    json2 = json.loads(text2)
    return find_diff_dict(json1, json2)


def find_diff_yaml(text1, text2):
    data1 = yaml.load(text1, Loader=yaml.CLoader)
    data2 = yaml.load(text2, Loader=yaml.CLoader)
    return find_diff_dict(data1, data2)


def find_diff_dict(dict1, dict2):
    return find_diff_dict_recursive(dict1, dict2)


def find_diff_dict_recursive(data1, data2):
    is_dict1 = type(data1) == dict
    is_dict2 = type(data2) == dict
    if not is_dict1 and not is_dict2:
        return None

    diff = []
    # ключ есть есть и там и там
    if is_dict1:
        for key in data1.keys():
            value1 = data1[key]
            is_value1_dict = type(value1) == dict
            value2 = None
            if data2 and key in data2:
                value2 = data2[key]

            is_value2_dict = type(value2) == dict

            next_level_diff = find_diff_dict_recursive(value1, value2)

            if is_dict2 and key in data2:
                # ключ есть в обоих

                # мап и мап
                # значение и мап
                # мап и значение
                # значение и значение
                if is_value1_dict and is_value2_dict:
                    diff.append(
                        Difference(key, STATUS_NOT_CHANGED,
                                   children=next_level_diff))
                elif not is_value1_dict and is_value2_dict:
                    diff.append(
                        Difference(key, STATUS_CHANGED, old_value=value1,
                                   children=next_level_diff))
                elif is_value1_dict and not is_value2_dict:
                    diff.append(
                        Difference(key, STATUS_CHANGED, value=value2,
                                   children=next_level_diff))
                else:
                    if value1 == value2:
                        diff.append(
                            Difference(key, STATUS_NOT_CHANGED, value=value1))
                    else:
                        diff.append(
                            Difference(key, STATUS_CHANGED, old_value=value1,
                                       value=value2))
            else:  # ключ есть только в 1
                if is_value1_dict:
                    # мапа
                    diff.append(
                        Difference(key, STATUS_REMOVED,
                                   children=next_level_diff))
                else:
                    # значение
                    diff.append(
                        Difference(key, STATUS_REMOVED, old_value=value1,
                                   children=next_level_diff))

    if is_dict2:
        for key in data2.keys():
            if not is_dict1 or key not in data1:
                # ключ есть только в 2
                value2 = data2[key]
                if type(value2) == dict:
                    next_level_diff = find_diff_dict_recursive(None, value2)
                    diff.append(
                        Difference(key, STATUS_ADDED,
                                   children=next_level_diff))

                else:
                    diff.append(
                        Difference(key, STATUS_ADDED, value=value2))

    return diff
