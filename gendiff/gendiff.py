import json

CONST_TEMPLATE = '  {} {} {}'


def generate_diff(file_path1, file_path2):
    with open(file_path1) as file1, open(file_path2) as file2:
        json1 = json.load(file1)
        json2 = json.load(file2)

        result = ['{']
        for key in json1.keys():
            if key not in json2:
                result.append(CONST_TEMPLATE.format('-', key, json1[key]))
            else:
                if json1[key] == json2[key]:
                    result.append(CONST_TEMPLATE.format(' ', key, json1[key]))
                else:
                    result.append(CONST_TEMPLATE.format("-", key, json1[key]))
                    result.append(CONST_TEMPLATE.format("+", key, json2[key]))

        for key in json2.keys():
            if key not in json1:
                result.append(CONST_TEMPLATE.format("+", key, json2[key]))

        result.append('}')

    return "\n".join(result)
