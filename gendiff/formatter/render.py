from typing import List

from gendiff.formatter.json import render_json
from gendiff.formatter.plain import render_plain
from gendiff.formatter.stylish import render_stylish

STYLE_STYLISH = 'stylish'
STYLE_PLAIN = 'plain'
STYLE_JSON = 'json'


def render(style: str, diff: List[dict]) -> str:
    if style == STYLE_STYLISH:
        return render_stylish(diff)

    if style == STYLE_PLAIN:
        return render_plain(diff)

    if style == STYLE_JSON:
        return render_json(diff)

    raise Exception("Invalid output format")
