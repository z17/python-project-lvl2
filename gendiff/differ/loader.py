import json


def get_data(file_path):
    with open(file_path) as file:
        return json.load(file)
