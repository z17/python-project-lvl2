import json

import yaml

from gendiff.differ.differ import FORMAT_JSON, FORMAT_YAML, FORMAT_YML


def parse(text, data_format):
    if data_format == FORMAT_JSON:
        return parse_json(text)

    if data_format == FORMAT_YAML or data_format == FORMAT_YML:
        return parse_yaml(text)

    raise Exception("Unknown file extension")


def parse_json(text: str):
    json1 = json.loads(text)
    return json1


def parse_yaml(text: str):
    data = yaml.load(text, Loader=yaml.CLoader)
    return data
