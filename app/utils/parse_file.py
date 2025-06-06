import json
from typing import Any


def parse_file(path: str, encoding: str = "utf-8") -> list[list[Any]]:
    objs = []
    with open(path, "r", encoding=encoding) as f:
        data = json.load(f)
        for obj in data:
            objs.append([*obj.values()])
    return objs
