import json
import yaml

FORMAT_JSON = 'json'
FORMAT_YAML = 'yml'


def find_diff(text1, text2, file_format):
    if file_format == FORMAT_JSON:
        return find_diff_json(text1, text2)

    if file_format == FORMAT_YAML:
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
    diff = []
    for key in dict1.keys():
        if key not in dict2:
            diff.append(('-', key, dict1[key]))
        else:
            if dict1[key] == dict2[key]:
                diff.append((' ', key, dict1[key]))
            else:
                diff.append(("-", key, dict1[key]))
                diff.append(("+", key, dict2[key]))

    for key in dict2.keys():
        if key not in dict1:
            diff.append(("+", key, dict2[key]))
    return diff
