import json
from typing import Any
from pathlib import WindowsPath


def parse_file(
    path: str | WindowsPath, encoding: str = "utf-8"
) -> list[list[Any]]:
    objs = []
    with open(path, "r", encoding=encoding) as f:
        data = json.load(f)
        if isinstance(data, list):
            for obj in data:
                objs.append([*obj.values()])
        else:
            objs.append([*data.values()])
    return objs
