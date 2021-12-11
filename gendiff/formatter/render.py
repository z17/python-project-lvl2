from typing import List

from gendiff.differ.Difference import Difference
from gendiff.formatter.plain import render_plain
from gendiff.formatter.stylish import render_stylish

STYLE_STYLISH = 'stylish'
STYLE_PLAIN = 'plain'


def render(style: str, diff: List[Difference]) -> str:
    if style == STYLE_STYLISH:
        return render_stylish(diff)

    if style == STYLE_PLAIN:
        return render_plain(diff)

    raise Exception("Invalid output format")
