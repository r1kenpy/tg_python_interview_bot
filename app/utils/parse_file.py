import json
from pathlib import Path
from typing import Any


def parse_file(path: str | Path, encoding: str = "utf-8") -> list[list[Any]]:
    objs = []
    with open(path, "r", encoding=encoding) as f:
        data = json.load(f)
        if isinstance(data, list):
            for obj in data:
                objs.append([*obj.values()])
        else:
            objs.append([*data.values()])
    return objs
