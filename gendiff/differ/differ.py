

def find_diff(json1, json2):
    diff = []
    for key in json1.keys():
        if key not in json2:
            diff.append(('-', key, json1[key]))
        else:
            if json1[key] == json2[key]:
                diff.append((' ', key, json1[key]))
            else:
                diff.append(("-", key, json1[key]))
                diff.append(("+", key, json2[key]))

    for key in json2.keys():
        if key not in json1:
            diff.append(("+", key, json2[key]))
    return diff
