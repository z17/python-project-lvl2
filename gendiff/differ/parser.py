import json

import yaml

from gendiff.differ.differ import FORMAT_JSON, FORMAT_YAML, FORMAT_YML


def parse(text1, text2, file_format):
    if file_format == FORMAT_JSON:
        return parse_json(text1, text2)

    if file_format == FORMAT_YAML or file_format == FORMAT_YML:
        return parse_yaml(text1, text2)

    raise Exception("Unknown file extension")


def parse_json(text1: str, text2: str):
    json1 = json.loads(text1)
    json2 = json.loads(text2)
    return json1, json2


def parse_yaml(text1: str, text2: str):
    data1 = yaml.load(text1, Loader=yaml.CLoader)
    data2 = yaml.load(text2, Loader=yaml.CLoader)
    return data1, data2
