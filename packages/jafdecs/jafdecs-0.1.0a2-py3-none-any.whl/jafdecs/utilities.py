import pathlib
from typing import Union


def filenotfound(path: Union[str, pathlib.Path]) -> bool:
    return not pathlib.Path(path).is_file()
